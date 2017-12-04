
# oTree Experiments

This repository contains a series of experimental economics games that I developed for Colby Economics Learning Laboratory
(CELL).

Currently, the codebase contains several demo games, included by default with the installation of oTree, but the following
games are ones that I made for CELL:

## Market_Wage

This game was created to study the changes in effort and wage rigidity through different market cycles.

It is a two-player game, with 12 rounds. One player is a **firm**, one player is a **worker**.
Throughout the 12 rounds, the market revenue varies, depending on whether the round is designated as a **boom**, a
**baseline** period, or a **recession**.

### Gameplay

- The firm chooses a wage
- The worker receives the wage, and chooses a corresponding result
- The firm's profit is calculated by the formula: **Firm Profit = (Revenue - Wage) * Effort**
- The worker's profit is calculated by the formula: **Worker Profit = Wage - Cost(Effort)**
- The cost function is a hardcoded discrete function

## UI Features

- A graph to help the firm make choices
- A slider bar for the worker and for the firm to help them choose wage and effort
- A Round history table, showing the choices and profits of both the firm and worker for each round


## oTree

oTree is a framework based on Python and Django that lets you build:

- Multiplayer strategy games, like the prisoner's dilemma, public goods game, and auctions
- Controlled behavioral experiments in economics, psychology, and related fields
- Surveys and quizzes

### Homepage
http://www.otree.org/
