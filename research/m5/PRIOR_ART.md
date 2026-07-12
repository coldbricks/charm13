# M5 Prior-Art Start

This is an initial collision map, not a completed novelty review.

## Fixed-horizon active hypothesis testing

Dhruva Kartik, Ashutosh Nayyar, and Urbashi Mitra, *Fixed-Horizon Active Hypothesis Testing*, arXiv:1911.06912.

Direct overlap: a fixed number of adaptively selected experiments followed by a hypothesis decision, with misclassification objectives. Required comparison: whether finite deterministic experiments, transcript total variation, exact adaptivity constants, minimal support, equality cases, or stability are treated.

## Active sequential hypothesis testing

Mohammad Naghshvar and Tara Javidi, *Active Sequential Hypothesis Testing*, Annals of Statistics 41(6), 2013, DOI 10.1214/13-AOS1144; arXiv:1203.4626.

Direct overlap: adaptive action selection in hypothesis testing. Main distinction to check: sequential stopping and asymptotic cost/error objectives versus M5's exact fixed-budget finite theorem.

Mohammad Naghshvar and Tara Javidi, *Sequentiality and Adaptivity Gains in Active Hypothesis Testing*, arXiv:1211.2291.

Direct overlap: explicit comparison of adaptive and nonadaptive action policies. This is a high-priority collision source for the phrase “adaptivity gap.”

## Sequential classification with costly features

Kirill Trapeznikov and Venkatesh Saligrama, *Supervised Sequential Classification Under Budget Constraints*, AISTATS 2013, PMLR 31:581-589.

Direct overlap: per-instance acquisition decisions under a budget and terminal classification. Required comparison: exact finite optimality, deterministic feature maps, static comparator, and sharp constants.

Jaromir Janisch, Tomas Pevny, and Viliam Lisy, *Classification with Costly Features as a Sequential Decision-Making Problem*, arXiv:1909.02564.

Direct overlap: hard and average feature budgets in sequential classification.

## Optimal classification trees

Emir Demirovic et al., *MurTree: Optimal Decision Trees via Dynamic Programming and Search*, JMLR 23(26), 2022.

Direct overlap: globally optimal classification trees under depth and node constraints, including a specialized depth-two algorithm. M5 Theorem 3.1 maps the adaptive objective exactly to weighted classification-tree error. Required comparison: whether the static-feature comparator and sharp finite adaptivity inequalities appear.

Laurent Hyafil and Ronald Rivest, *Constructing Optimal Binary Decision Trees is NP-Complete*, Information Processing Letters 5(1):15-17, 1976.

Direct overlap: foundational decision-tree complexity. Objective differs: expected number of tests for identification. Required comparison before any complexity claim.

## Precedence-constrained decision trees

Michal Szyfelbein and Dariusz Dereniowski, *Precedence-Constrained Decision Trees and Coverings*, arXiv:2602.21312, 2026.

Direct overlap: tests with predecessor constraints and adaptive decision trees. Their advertised objectives are worst-case or average identification time, with approximation and hardness results. M5's guarded/open distinction must be compared line by line; filesystem-prefix vocabulary does not establish a gap.

## What remains to be searched

Blackwell comparison of experiments; Le Cam deficiency under restricted experiment classes; exact adaptivity gaps in active feature acquisition; equivalence-class determination and adaptive submodularity; decision-tree versus static-feature approximation ratios; signed transportation and circulation decompositions; equality and stability for `L1` triangle inequalities; pointer/address functions in query complexity.

## Current claim discipline

The generic model is known territory. The support theorem, exact `1-1/K` finite extremal law, four-world equality classification, and any eventual stability theorem remain “proved in the frozen model, novelty unresolved” until primary-source collision is complete.
