# WebCrypto Session Key Hardening

Status: candidate

Use this workflow when a public issue asks for session-only WebCrypto keys to be non-extractable, and the relevant key import or derivation paths are visible in public client code.

## Trigger

Good fits:

- an issue explicitly identifies `extractable: true` on session-only keys
- ECDH, ECDSA, AES-GCM, or shared-secret paths are easy to isolate
- registration, backup, or explicit export paths can be kept unchanged
- the fix is a narrow boolean change with clear build validation

Do not use this as a general cryptography redesign or certified security guarantee.

## Inputs

- Public issue describing the key extractability concern.
- WebCrypto import, unwrap, derive, and export call sites.
- Build/test commands from the target repository.
- Any documented key lifecycle or registration flow.

Never request private keys, credentials, account access, production secrets, or real user data.

## Workflow

1. Map each WebCrypto key call site to its lifecycle role.
2. Separate session-only operational keys from registration, backup, export, or wrapping flows.
3. Set session-only imported or derived keys to `extractable: false`.
4. Leave legitimate export paths unchanged unless the issue explicitly covers them.
5. Keep the diff minimal and avoid unrelated crypto refactors.
6. Run the target build/test command.
7. Report unrelated pre-existing failures separately instead of hiding them.

## Validation

Target repo checks should include at least:

```bash
npm run build
git diff --check
```

When available, also run focused tests for:

- key import
- key derivation
- message encryption/decryption
- registration or key export flows that must stay functional

Expected review notes:

- identify which call sites were changed
- state which export/registration paths were intentionally not changed
- avoid claiming the app is secure because of this single hardening step

## Failure Modes

Stop or revise when:

- a key must be exportable for a documented product flow
- the app serializes or backs up the same key later in the lifecycle
- the change breaks registration, recovery, migration, or wrapped-key storage
- validation requires private credentials or production data
- the issue requires broader cryptographic design review beyond a bounded PR

## Evidence

This candidate is based on a merged public WebCrypto hardening PR:

- Source issue: https://github.com/RoshanDavis/whisper/issues/8
- Merged PR: https://github.com/RoshanDavis/whisper/pull/9
- Result: maintainer merged the scoped `extractable: false` session-key change.
