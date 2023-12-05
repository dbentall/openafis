# distutils: language = c++

from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp cimport bool
from libc.stdint cimport uint8_t

# Declare the C++ class and its methods


cdef extern from "Dimensions.h" namespace "OpenAFIS":
    pass

cdef extern from "FastMath.cpp" namespace "OpenAFIS":
    pass

cdef extern from "FastMath.h" namespace "OpenAFIS":
    pass

cdef extern from "Field.h" namespace "OpenAFIS":
    pass

cdef extern from "Fingerprint.h" namespace "OpenAFIS":
    cdef cppclass Fingerprint:
        Fingerprint(size_t, size_t) except +

cdef extern from "Log.h" namespace "OpenAFIS":
    pass

cdef extern from "Match.cpp" namespace "OpenAFIS":
    pass

cdef extern from "Match.h" namespace "OpenAFIS":
    cdef cppclass MatchSimilarity:
        MatchSimilarity() except +
        void compute(uint8_t& result, const Fingerprint& probe, const Fingerprint& candidate, Param param) const

cdef extern from "MatchMany.cpp" namespace "OpenAFIS":
    pass

cdef extern from "MatchMany.h" namespace "OpenAFIS":
    pass

cdef extern from "Minutia.h" namespace "OpenAFIS":
    pass

cdef extern from "MinutiaPoint.h" namespace "OpenAFIS":
    pass

cdef extern from "OpenAFIS.cpp" namespace "OpenAFIS":
    pass

cdef extern from "OpenAFIS.h" namespace "OpenAFIS":
    pass

cdef extern from "Param.h" namespace "OpenAFIS":
    cdef cppclass Param:
        short MaximumLocalDistance
        short MaximumGlobalDistance
        unsigned int MinimumMinutiae
        int MaximumRotations
        float MaximumAngleDifference
        float MaximumDirectionDifference

cdef extern from "Render.cpp" namespace "OpenAFIS":
    pass

cdef extern from "Render.h" namespace "OpenAFIS":
    pass

cdef extern from "StringUtil.h" namespace "OpenAFIS":
    pass

cdef extern from "Template.cpp" namespace "OpenAFIS":
    pass

cdef extern from "Template.h" namespace "OpenAFIS":
    pass

cdef extern from "TemplateCSV.cpp" namespace "OpenAFIS":
    pass

cdef extern from "TemplateCSV.h" namespace "OpenAFIS":
    pass

cdef extern from "TemplateISO19794_2_2005.cpp" namespace "OpenAFIS":
    pass

cdef extern from "TemplateISO19794_2_2005.h" namespace "OpenAFIS":
    cdef cppclass TemplateISO19794_2_2005[IdType, FingerprintType]:
        TemplateISO19794_2_2005(const IdType id) except +
        bool load(const string&)
        vector[FingerprintType] fingerprints()

cdef extern from "ThreadPool.h" namespace "OpenAFIS":
    pass

cdef extern from "Triplet.cpp" namespace "OpenAFIS":
    pass

cdef extern from "Triplet.h" namespace "OpenAFIS":
    pass

cdef extern from "TripletScalar.cpp" namespace "OpenAFIS":
    pass

cdef extern from "TripletScalar.h" namespace "OpenAFIS":
    pass
