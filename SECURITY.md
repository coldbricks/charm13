# Security

## What CHARM13 protects

Cover stories and detection of **obvious** cover failure (T0–T1).
Confidentiality of volume contents depends entirely on the volume tool
(VeraCrypt or whatever you put behind the payload path).

## What CHARM13 does not protect

- Compelled disclosure of passwords (without a carefully used hidden volume)
- Full-disk forensic labs (T4)
- OS leakage: recent files, thumbnails, Defender history, shellbags, cloud sync
- Weak passwords
- Operator mistakes (`--i-know` on a blown tree)

## Reporting

If you find a way to make `charm bench` pass while shipping a cover that
fails the documented checks, open an issue with a minimal tree.

Do not send real personal data or real volume passwords.

## Crypto

CHARM13 does not implement a data cipher. Review VeraCrypt (or your chosen
volume format) separately.
