# Upstream source snapshot

These files are byte-for-byte snapshots from the paper's official repository:

- Repository: `https://github.com/ZusenXu/GFS-DRO`
- Commit: `6f9fb5c9e432b5cc6ad62916b36f102984b4d076`
- `README.md` SHA-256:
  `7cd756c94dd22fa36c71f3149eef7ad80e246ec8d96db4569c09856de9269a7f`
- `CIFAR10_feature_regression/Multiclass_classification.py` SHA-256:
  `c8bf279ce59d8a5a4ebcfd18c03e13211ba57dd1564ff512dd2bad4d1db1ca52`

The upstream tree has no lockfile, dependency file, declared Python version, or
top-level run command. The CIFAR script downloads and extracts features but then
requires a separate `cifar10_resnet50_features.pth` file that is neither created
nor tracked. It also contains one repeat although the paper's uncertainty
language is broader. The snapshot is a primary-source reference, not accepted
evidence by itself.

