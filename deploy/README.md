# Deploy

Deployment manifests — compose files, Kubernetes objects, platform descriptors —
kept outside the package because nothing here is imported at runtime.

Deliberately empty in this template: a manifest encodes a deployment shape that
depends on where the thing actually runs, and a wrong one is more expensive than
a missing one. Five of the thirteen surveyed repositories carry a deploy
manifest, so its absence is not a defect — but the moment yours exists, this is
where it goes.
