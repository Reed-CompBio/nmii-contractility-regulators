# NMII Contractility Regulators

This repo contains code and supplementary networks for the paper

**From network analysis to experimental validation: identification of regulators of non-muscle myosin II contractility using the folded-gastrulation signaling pathway** by Zhao et al. ([preprint](https://www.researchsquare.com/article/rs-3140226/v1))

*Under revision at BMC Molecular Biology*


### Supplementary Networks

The networks were created using [GraphSpace](https://graphspace.org/), a collaborative interactive platform for network sharing. All interactions shown in the networks are from the protein-protein interactome. (Note: the number in each title is random, and a result of the fact that all uploaded graphs need unique titles).

[Steiner Network](https://graphspace.org/graphs/35568): Gray nodes are positives; red nodes are candidate proteins that connect positives.

[Paths to NMII Network](https://graphspace.org/graphs/35578): Gray nodes are positives; green nodes are candidate proteins on some path from a positive to NMII.

[Ranked Paths Network](https://graphspace.org/graphs/35579): Blue nodes are the top-ranked candidate proteins that are closest to many positives; NMII is shown in gray for reference.

[Combined Network](https://graphspace.org/graphs/35583): Node size indicates the number of methods that found the predicted protein (large white nodes indicate proteins found by all three methods). Gray: positive (known) proteins; red: proteins predicted by only the Steiner method; green: proteins predicted by only paths to NMII; blue: proteins predicted by only the ranked paths approach; yellow: proteins predicted by Steiner & paths to NMII; cyan: proteins predicted by paths to NMII and ranked paths; magenta: proteins predicted by Steiner and ranked paths methods.

[Oya Network](https://graphspace.org/graphs/35588): Oya’s direct interacting partners are shown along with any interactions among those neighbors. The network includes the positive Sqh (gray) and two Ubiquitinases (green) that are found by at least one of the three algorithms.

If you have trouble viewing the networks in Chrome, try Firefox or Safari browsers.


### Code
