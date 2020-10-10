#ifndef STRINGUTIL_H
#define STRINGUTIL_H


//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#include <algorithm>
#include <iostream>
#include <string>


//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class StringUtil
{
public:
    static std::string lower(const std::string& s)
    {
        auto _s = s;
        std::transform(_s.begin(), _s.end(), _s.begin(), [](const unsigned char c) { return std::tolower(c); });
        return _s;
    }

    static bool contains(const std::string& s, const std::string& part) { return s.find(part) != std::string::npos; }
    static std::string center(const std::string& s, const int width = 80) { return std::string((width - s.length()) / 2, ' ') + s; }

    template <typename... A> static std::string format(const std::string& format, A... args)
    {
        const auto size = snprintf(nullptr, 0, format.c_str(), args...) + 1;
        if (size <= 0) {
            return "";
        }
        const std::unique_ptr<char[]> buf(new char[size]);
        snprintf(buf.get(), size, format.c_str(), args...);
        return std::string(buf.get(), buf.get() + size - 1);
    }
};

#endif // STRINGUTIL_H
