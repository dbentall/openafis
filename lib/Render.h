#ifndef RENDER_H
#define RENDER_H


//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#include "Fingerprint.h"
#include "Param.h"

#include <string>


//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
namespace OpenAFIS
{

class Render
{
public:
    static bool minutiae(std::string& svg, const FingerprintRenderable& fp);
    static bool pairs(std::string& svg1, std::string& svg2, const FingerprintRenderable& fp1, const FingerprintRenderable& fp2, Param param);
    static bool all(std::string& svg1, std::string& svg2, const FingerprintRenderable& fp1, const FingerprintRenderable& fp2, Param param);

private:
    static void addMinutiae(std::string& svg, const FingerprintRenderable& fp);
    static void addPairs(std::string& svg1, std::string& svg2, const FingerprintRenderable& fp1, const FingerprintRenderable& fp2, Param param);
    static void open(std::string& svg, const Dimensions& dimensions);
    static void close(std::string& svg);
};
}

#endif // RENDER_H
