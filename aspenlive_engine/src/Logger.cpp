// Copyright (c) 2008-2026 OpenShot Studios, LLC
// SPDX-License-Identifier: LGPL-3.0-or-later
#include "Logger.h"
#include "Settings.h"
#if USE_RESVG == 1
#include "ResvgQt.h"
#endif
#include <algorithm>
#include <cctype>
#include <cstdio>
#include <cstdlib>
#include <ctime>
#ifdef _WIN32
#include <filesystem>
#endif
#ifndef _WIN32
#include <sys/stat.h>
#endif
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <thread>

using namespace openshot;
namespace {
int ParseLevel(std::string value) {
    std::transform(value.begin(), value.end(), value.begin(),
        [](unsigned char c) { return std::toupper(c); });
    if (value == "DEBUG") return Logger::LevelDebug;
    if (value == "INFO") return Logger::LevelInfo;
    if (value == "WARNING") return Logger::LevelWarning;
    if (value == "ERROR") return Logger::LevelError;
    if (value == "CRITICAL") return Logger::LevelCritical;
    if (value == "OFF") return Logger::LevelOff;
    throw std::invalid_argument("Invalid logging level: " + value);
}
const char* LevelName(Logger::Level level) {
    switch (level) {
    case Logger::LevelDebug: return "DEBUG";
    case Logger::LevelInfo: return "INFO";
    case Logger::LevelWarning: return "WARNING";
    case Logger::LevelError: return "ERROR";
    case Logger::LevelCritical: return "CRITICAL";
    default: return "OFF";
    }
}
std::tm LocalTime(std::time_t now) {
    std::tm result{};
#ifdef _WIN32
    localtime_s(&result, &now);
#else
    localtime_r(&now, &result);
#endif
    return result;
}
}

Logger* Logger::Instance() {
    // Retain the logger through static destruction, including crash reporting.
    static Logger* instance = new Logger;
    return instance;
}

Logger::Logger() : legacy_settings(Settings::Instance()) {
    // Parse each variable once; malformed values do not hide valid fallbacks.
    for (const char* key : {"OPENSHOT_LOG_LEVEL", "OPENSHOT_LOG_FILE_LEVEL",
         "OPENSHOT_LOG_CONSOLE_LEVEL", "LIBOPENSHOT_LOG_LEVEL",
         "LIBOPENSHOT_LOG_FILE_LEVEL", "LIBOPENSHOT_LOG_CONSOLE_LEVEL",
         "ASPENLIVE_LOG_LEVEL", "ASPENLIVE_LOG_FILE_LEVEL",
         "ASPENLIVE_LOG_CONSOLE_LEVEL"}) {
        const char* value = std::getenv(key);
        if (!value) continue;
        try {
            int level = ParseLevel(value);
            std::string name(key);
            if (name.find("CONSOLE") == std::string::npos) file_level = level;
            if (name.find("FILE") == std::string::npos) {
                console_level = level;
                console_configured = true;
            }
        } catch (const std::invalid_argument&) {
            std::cerr << "libopenshot: ignoring invalid " << key << "=" << value << '\n';
        }
    }
#ifdef _WIN32
    // Windows environment paths are UTF-16; avoid the locale-dependent narrow getenv.
    const wchar_t* path = _wgetenv(L"ASPENLIVE_LOG_FILE");
    if (!path) path = _wgetenv(L"LIBOPENSHOT_LOG_FILE");
    if (path) {
        try { Path(std::filesystem::path(path).u8string()); }
        catch (const std::exception&) {
            std::cerr << "libopenshot: invalid LIBOPENSHOT_LOG_FILE path\n";
        }
    }
#else
    const char* path = std::getenv("ASPENLIVE_LOG_FILE");
    if (!path) path = std::getenv("LIBOPENSHOT_LOG_FILE");
    if (path) Path(path);
#endif
#if USE_RESVG == 1
    ResvgRenderer::initLog();
#endif
}

int Logger::ConsoleLevel() const {
    // Preserve the old explicit Settings API and presence-based environment alias.
    if (!console_configured && legacy_settings->DEBUG_TO_STDERR) return LevelDebug;
    return console_level;
}
bool Logger::ShouldLog(Level level) const {
    return level != LevelOff && ((file_open && level >= file_level) || level >= ConsoleLevel());
}
void Logger::SetFileLevel(std::string level) { file_level = ParseLevel(level); }
void Logger::SetConsoleLevel(std::string level) {
    console_level = ParseLevel(level);
    console_configured = true;
}
void Logger::Enable(bool enabled) { file_level = enabled ? LevelDebug : LevelOff; }

static std::uintmax_t ExistingLogBytes(const std::string& path) {
    if (path.empty()) return 0;
#ifdef _WIN32
    try {
        std::error_code error;
        auto size = std::filesystem::file_size(std::filesystem::u8path(path), error);
        return error ? 0 : static_cast<std::uintmax_t>(size);
    } catch (const std::exception&) {
        return 0;
    }
#else
    struct stat info;
    if (::stat(path.c_str(), &info) != 0 || info.st_size < 0) return 0;
    return static_cast<std::uintmax_t>(info.st_size);
#endif
}

bool Logger::OpenFile(bool truncate) {
    log_file.clear();
    try {
#ifdef _WIN32
        log_file.open(std::filesystem::u8path(file_path),
            std::ios::out | (truncate ? std::ios::trunc : std::ios::app));
#else
        // POSIX paths already use UTF-8 bytes. Avoid std::filesystem, which
        // requires macOS 10.15 even when compiling with C++17 enabled.
        log_file.open(file_path, std::ios::out | (truncate ? std::ios::trunc : std::ios::app));
#endif
    } catch (const std::exception&) {
        std::cerr << "libopenshot: invalid log file path: " << file_path << '\n';
        return false;
    }
    file_open = log_file.is_open();
    if (!file_open) {
        std::cerr << "libopenshot: unable to open log file: " << file_path << '\n';
        return false;
    }
    log_file.seekp(0, std::ios::end);
    auto now = LocalTime(std::time(nullptr));
    // Keep these markers intact for openshot-qt's existing crash recovery scanner.
    log_file << "------------------------------------------\n"
             << "libopenshot logging: " << std::put_time(&now, "%a %b %d %H:%M:%S %Y") << '\n'
             << "------------------------------------------" << std::endl;
    return true;
}

void Logger::WriteFileLine(const std::string& text) {
    if (!log_file.is_open()) return;
    const auto position = log_file.tellp();
    if (position >= 0 && position + static_cast<std::streamoff>(text.size()) > kMaxLogBytes)
        Rotate();
    if (log_file.is_open()) log_file << text << std::flush;
}

void Logger::FlushRepeats() {
    if (repeat_count <= 0) return;
    auto now = LocalTime(std::time(nullptr));
    std::ostringstream record;
    record << std::put_time(&now, "%Y-%m-%d %H:%M:%S") << " INFO [log] repeated "
           << repeat_count << " times\n";
    repeat_count = 0;
    const auto text = record.str();
    if (log_file.is_open()) log_file << text << std::flush;
    if (LevelInfo >= ConsoleLevel()) std::clog << text << std::flush;
}

void Logger::Rotate() {
    // The active file is already at the cap, so renaming it does not copy a
    // multi-gigabyte log. An oversized file is truncated in Path() instead.
    if (log_file.is_open()) log_file.close();
    file_open = false;
    const std::string newer = file_path + ".1";
    const std::string older = file_path + ".2";
#ifdef _WIN32
    std::error_code error;
    std::filesystem::remove(std::filesystem::u8path(older), error);
    std::filesystem::rename(std::filesystem::u8path(newer), std::filesystem::u8path(older), error);
    std::filesystem::rename(std::filesystem::u8path(file_path), std::filesystem::u8path(newer), error);
#else
    ::remove(older.c_str());
    ::rename(newer.c_str(), older.c_str());
    ::rename(file_path.c_str(), newer.c_str());
#endif
    OpenFile(true);
}

void Logger::Path(std::string path) {
    const std::lock_guard<std::recursive_mutex> lock(loggerMutex);
    if (path == file_path && file_open) return;
    FlushRepeats();
    last_payload.clear();
    repeat_count = 0;
    file_open = false;
    if (log_file.is_open()) log_file.close();
    file_path = path;
    if (path.empty()) return;
    // Replace an already-huge file in place. Never copy it to rotate.
    const bool truncate = ExistingLogBytes(path) > static_cast<std::uintmax_t>(kMaxLogBytes);
    OpenFile(truncate);
}
void Logger::LogToFile(std::string message) {
    // Deliberately retain the existing crash-write path (no level filter or new lock).
    if (log_file.is_open()) log_file << message << std::flush;
}
void Logger::Log(std::string message, Level level) {
    if (!ShouldLog(level)) return;
    const std::lock_guard<std::recursive_mutex> lock(loggerMutex);
    while (!message.empty() && (message.back() == '\n' || message.back() == '\r'))
        message.pop_back();
    std::replace(message.begin(), message.end(), '\n', ' ');
    if (message == last_payload && level == last_level) {
        ++repeat_count;
        return;
    }
    FlushRepeats();
    last_payload = message;
    last_level = level;
    auto now = LocalTime(std::time(nullptr));
    std::ostringstream record;
    record << std::put_time(&now, "%Y-%m-%d %H:%M:%S") << ' '
           << LevelName(level) << " [log] " << message << '\n';
    const auto text = record.str();
    if (level >= file_level) WriteFileLine(text);
    if (level >= ConsoleLevel()) std::clog << text << std::flush;
}
void Logger::Close() {
    const std::lock_guard<std::recursive_mutex> lock(loggerMutex);
    FlushRepeats();
    last_payload.clear();
    file_level = LevelOff;
    console_level = LevelOff;
    console_configured = true;
    file_open = false;
    if (log_file.is_open()) log_file.close();
}

// Append debug information
void Logger::AppendDebugMethod(std::string method_name,
				  std::string arg1_name, float arg1_value,
				  std::string arg2_name, float arg2_value,
				  std::string arg3_name, float arg3_value,
				  std::string arg4_name, float arg4_value,
				  std::string arg5_name, float arg5_value,
				  std::string arg6_name, float arg6_value)
{
	if (!ShouldLog(LevelDebug))
		// Don't do anything
		return;

	{
		// Create a scoped lock, allowing only a single thread to run the following code at one time
		const std::lock_guard<std::recursive_mutex> lock(loggerMutex);

		std::stringstream message;
		message << std::fixed << std::setprecision(4);

		// Construct message
		message << method_name << " (";

		if (arg1_name.length() > 0)
			message << arg1_name << "=" << arg1_value;

		if (arg2_name.length() > 0)
			message << ", " << arg2_name << "=" << arg2_value;

		if (arg3_name.length() > 0)
			message << ", " << arg3_name << "=" << arg3_value;

		if (arg4_name.length() > 0)
			message << ", " << arg4_name << "=" << arg4_value;

		if (arg5_name.length() > 0)
			message << ", " << arg5_name << "=" << arg5_value;

		if (arg6_name.length() > 0)
			message << ", " << arg6_name << "=" << arg6_value;

		message << ")\n";

		Log(message.str(), LevelDebug);
	}
}
