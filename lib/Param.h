#ifndef PARAM_H
#define PARAM_H


//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#include "FastMath.h"
#include "Field.h"


//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
namespace OpenAFIS
{

class Param
{
public:
    Field::MinutiaDistanceType MaximumLocalDistance = 12; // NJH-TODO require scaling
    Field::MinutiaDistanceType MaximumGlobalDistance = 12; // "
    uint MinimumMinutiae = 4;
    int MaximumRotations = 3; // 3 = best accuracy, [1,2] faster match times
    float MaximumAngleDifference = FastMath::PI / 6;
    float MaximumDirectionDifference = FastMath::PI / 4;

    static constexpr uint MaximumConcurrency = 256; // 1 = single-threaded
    static constexpr bool EnableSIMD = false; // NJH-TODO: not supported yet

    Field::AngleType maximumAngleDifference()
    {
        if constexpr (std::is_same_v<Field::AngleType, float>) {
            return MaximumAngleDifference;
        }
        if constexpr (std::is_same_v<Field::AngleType, int16_t>) {
            return static_cast<Field::AngleType>(round(MaximumAngleDifference * FastMath::Radians8));
        }
    }

    Field::AngleType maximumDirectionDifference()
    {
        if constexpr (std::is_same_v<Field::AngleType, float>) {
            return MaximumDirectionDifference;
        }
        if constexpr (std::is_same_v<Field::AngleType, int16_t>) {
            return static_cast<Field::AngleType>(round(MaximumDirectionDifference * FastMath::Radians8));
        }
    }

private:
    // A very limited, but constexpr, round function to help with params...
    static constexpr Field::AngleType round(const float x) { return static_cast<Field::AngleType>(x >= 0.0f ? x + 0.5f : x - 0.5f); }
};
}

#endif // PARAM_H
