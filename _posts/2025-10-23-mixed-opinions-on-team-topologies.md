---
title: "Mixed Opinions on Team Topologies"
date: 2025-01-05T09:36:00-04:00
categories:
  - books
tags:
  - python
  - tach
  - dependency management
excerpt_separator: <!--more-->
---

I just reread Team Topologies (bought the new 2nd edition after misplacing my copy) and I have the same mixed reaction: I strongly agree with two foundational points and strongly disagree with two others and I'm curious if I'm the outlier. 
<!--more-->

I'll try to present the book's perspective neutrally up front and add some commentary afterward.

### Cognitive Load

- Team cognitive load matters. Slice up the work so each team owns a small, coherent slice of the system that fits its cognitive capacity and consider the total cumulative cognitive load on a team before pushing more work their way. Use dedicated teams for complicated subsystems so stream-aligned teams are not overloaded.

## Unnecessary Conversation

- Not all communication is good. Make communication intentional with clear team interfaces and explicit interaction modes (collaboration, x-as-a-service, facilitating) so attention stays focused and handoffs are minimized. If necessary, physically move teams to discourage or restrict "unnecessary communication". 

## Organizing Teams to Drive a Desired Architecture (aka the "Inverse Conway Maneuver")

- Reorganizing teams (applying the "Inverse Conway Maneuver") to redefine team boundaries and communication paths will encourage the creation of a system that aligns with the desired architecture.

## Individual vs. Team-Level Incentives

- Teams are the smallest unit of delivery and reward. Organizations that manage by objective with "Performance Management" cultures that use individual performance ratings and merit bonuses create unhealthy environments and result in worse outcomes than team-level incentives 

![Output of `tach show`](https://github.com/gauge-sh/tach/blob/main/docs/assets/tach_show.png?raw=true)

[team-topologies-site]: https://github.com/gauge-sh/tach
[pipenv-site]: https://pipenv.pypa.io
[poetry-site]: https://python-poetry.org/
