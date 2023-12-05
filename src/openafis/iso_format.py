import struct

from pydantic import BaseModel


class Minutia(BaseModel):
    type: int
    x: int
    y: int
    angle: int
    quality: int


class Fingerprint(BaseModel):
    position: int
    quality: int
    minutiae: list[Minutia]


class ISOFormat(BaseModel):
    width: int
    height: int
    resolution_x: int
    resolution_y: int
    fingerprints: list[Fingerprint]

    @classmethod
    def from_iso_file(cls, path):
        fingerprints = []

        with open(path, "rb") as f:
            header = f.read(8)
            if header != b"FMR\x00 20\x00":
                raise ValueError("Invalid ISO 19794-2 file")

            # Read the header
            (
                _,
                _,
                width,
                height,
                resolution_x,
                resolution_y,
                fingerprint_count,
                _,
            ) = struct.unpack(">IHHHHHBB", f.read(16))

            # Read the fingerprints
            for _ in range(fingerprint_count):
                position, _, quality, minutiae_count = struct.unpack(">BBBB", f.read(4))
                minutiae = []
                for _ in range(minutiae_count):
                    type_x, rfu_y, angle, quality = struct.unpack(">HHBB", f.read(6))
                    x = type_x & 0x3FFF  # Lower 14 bits
                    # Extract type
                    type_ = type_x >> 14  # Upper 2 bits
                    y = rfu_y & 0x3FFF  # Lower 14 bits
                    minutiae.append(
                        Minutia(type=type_, x=x, y=y, angle=angle, quality=quality)
                    )
                fingerprints.append(
                    Fingerprint(
                        position=position,
                        quality=quality,
                        minutiae=minutiae,
                    )
                )

        return cls(
            width=width,
            height=height,
            resolution_x=resolution_x,
            resolution_y=resolution_y,
            fingerprints=fingerprints,
        )

    def to_iso_file(self, path):
        with open(path, "wb") as f:
            f.write(self.to_iso_bytes())

    def to_iso_bytes(self) -> bytes:
        # n_fingerprints * (fingerprint_header + n_minutiae * minutiae)
        fingerprint_lengths = [
            4 + len(fingerprint.minutiae) * 6 for fingerprint in self.fingerprints
        ]
        # pre-header + header + sum(fingerprint_lengths) + footer
        total_length = 8 + 16 + sum(fingerprint_lengths) + 2

        # Pre-header
        out = b"FMR\x00 20\x00"
        out += struct.pack(
            ">IHHHHHBB",
            total_length,
            0,
            self.width,
            self.height,
            self.resolution_x,
            self.resolution_y,
            len(self.fingerprints),
            0,
        )
        for fingerprint in self.fingerprints:
            out += struct.pack(
                ">BBBB",
                fingerprint.position,
                0,
                fingerprint.quality,
                len(fingerprint.minutiae),
            )
            for minutia in fingerprint.minutiae:
                type_x = (minutia.type << 14) | minutia.x
                rfu_y = minutia.y
                out += struct.pack(
                    ">HHBB",
                    type_x,
                    rfu_y,
                    minutia.angle,
                    minutia.quality,
                )
        # Footer
        out += b"\x00\x00"
        return out


if __name__ == "__main__":
    import sys
    import json

    

    # sys.argv = [
    #     "pyso.py",
    #     "/powerplant/workspace/hrrdxb/Scratch/openafis/data/valid/fvc2004/DB1_B/101_1.iso",
    #     "test.iso",
    # ]

    # if len(sys.argv) < 2:
    #     print("Reads ISO file and writes to output file")
    #     print("Usage: python pyso.py <path to ISO 19794-2 file> [<output file>]")
    #     sys.exit(1)

    # path = sys.argv[1]
    # fingerprints = ISOFormat.from_iso_file(path)

    # if len(sys.argv) > 2:
    #     out_path = sys.argv[2]
    #     fingerprints.to_iso_file(out_path)
    #     fingerprints2 = ISOFormat.from_iso_file(out_path)
    #     if fingerprints == fingerprints2:
    #         print("ISO files are equal")
    #     else:
    #         print("ISO files are not equal")
    #         print("Original:")
    #         print(json.dumps(fingerprints.dict(), indent=4))
    #         print("New:")
    #         print(json.dumps(fingerprints2.dict(), indent=4))
    # else:
    #     print(json.dumps(fingerprints.dict(), indent=4))
