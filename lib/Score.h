#ifndef SCORE_H
#define SCORE_H


//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#include "Template.h"


//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Score
{
public:
    unsigned int compute(const Template& probe, const Template& candidate);
    unsigned int compute(const Fingerprint& probe, const Fingerprint& candidate);

private:
    void findPairs(Triplet::Pairs& pairs, const Triplet& probeT, const Fingerprint& candidate) const;
};

#endif // SCORE_H
