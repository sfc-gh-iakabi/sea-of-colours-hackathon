"""weapon_plays — YOUR agent's weapon moves. This is the only file you edit.

Everything else was installed once by ``forge_install.py``. To add a weapon or
a move, add a ``WeaponPlay`` below. Nothing else in the harness needs touching:
the menu group, the wire move, the replay tag, the doctrine and the rationale
are all derived from what you write here.

Each move is four decisions:

  WHEN           always | redsign_mine | redsign_theirs | other
                 The board condition. ``redsign_mine`` = a pure WE found is
                 live (we are defending it). ``redsign_theirs`` = a rival
                 found it (we are attacking it).

  HOUR           super_early (H1) | early (H1-2) | mid | late | last_night
                 Position in the move list IS the hour, so this is a hard
                 constraint. An 8h EMP cloud past H2 has no night left to use;
                 a chaff has to land on the hour they were going to act.

  COMBINES_WITH  smash_grab | blind_grab | probe | chain | standalone
                 Which existing play this borrows geometry from, so the option
                 has real coordinates rather than invented ones.

  WHY            One sentence: what firing this BUYS. Yours, in your words.
                 The full rationale the model reads is composed from this plus
                 the weapon's mechanics plus the alternative it beats — that
                 last part depends on what else is on tonight's menu, which is
                 why the machinery adds it rather than you.

Name the move whatever you like. It is public: it shows up in the game log as
the night resolves, in the lab's frozen-turn journals and in the season cards.
Be as silly as you like about the TONE and never about the CONTENT — calling a
cautious vision move ``NUKE`` tells the model that option is aggressive, and
that is a bug you will spend an hour not finding.

Check yourself any time with:

    python skills/soc-agent-forge/scripts/check_wiring.py <your_label>
"""

from __future__ import annotations

from typing import Tuple

from .weapon_forge import EconomyPolicy, WeaponPlay


# ── how the weapons get PAID FOR ──────────────────────────────────────────
# The defaults are the conservative reading and are right for most teams:
# fund what you fire, never buy ordnance you have no play for, and never pull
# your last harvester off red to fetch currency.
#
#   soc will buy the cheapest weapon you declared the moment it can afford it,
#   set the stockpile cap to 0 for any weapon you did NOT declare, and ask for
#   blue on any night your rack cannot fire.
#
# Change something only if you mean it. `hold_at={"chaff": 1}` caps the rack at
# one; `seek_blue_when_rack_empty=False` reverts to the baseline's behaviour of
# only topping up when the VAULT is short.
# EMP is 200 blue; buy_asap + never_buy_what_you_cannot_fire are already the
# defaults. The two changes below fund it: seek blue EVERY night (the default
# only seeks when the rack is empty, which starves the 2nd EMP and the refill
# after firing), and cap the stockpile at 2 (a decisive salvo, not a hoard
# against the public 600-blue cap). We also declare SNAP now, so the economy
# is allowed to buy it (it caps undeclared weapons at 0). Cap: 2 EMP + 2 SNAP =
# 600 blue if fully stocked. EMP + SNAP share geometry and both fit under the
# 600 public cap (2 emp + 2 snap = 600). Chaff was dropped: at 300 blue it lands
# emp on the cap boundary so emp could never arm, and its denial role overlaps
# LIGHTS_DOWN / BLIND_THE_FINDER anyway. Aggressive across every case without it.
ECONOMY = EconomyPolicy(seek_blue_always=True, hold_at={"emp": 2, "snap": 2})


PLAYS: Tuple[WeaponPlay, ...] = (
    WeaponPlay(
        play_id="LIGHTS_DOWN",
        weapon="emp",
        when="redsign_theirs",
        hour="super_early",
        targets="redsign",
        probe_the_comb=True,
        take_the_ground=True,
        combines_with="blind_grab",
        why=(
            "covering their smear at H1 locks them out of their own pure for "
            "eight hours; then we comb the ground they cannot reach \u2014 the "
            "exposed edge now, or the interior once our own cloud clears"
        ),
    ),
    WeaponPlay(
        play_id="BLIND_THE_FINDER",
        weapon="snap",
        when="redsign_theirs",
        hour="super_early",
        targets="finder_probe",
        min_targets=1,
        combines_with="blind_grab",
        why=(
            "when a rival lights a pure we cannot see, the eye that found it "
            "is the only target we can name; snapping it at hour one refuses "
            "their drop for lack of live vision, then a paired blind-grab combs "
            "the smear they can no longer reach"
        ),
    ),
    WeaponPlay(
        play_id="PURE_TRAP",
        weapon="snap",
        when="always",
        hour="super_early",
        targets="contested_pure",
        min_targets=1,
        combines_with="smash_grab",
        why=(
            "a pure we can see that a rival probe also watches is the one cell "
            "whose occupation is predictable \u2014 they smash-and-grab it at "
            "hour one; snapping it refuses that landing and damages the hull, "
            "then a smash-grab lands on the cold pure at hour two and banks it"
        ),
    ),
    WeaponPlay(
        play_id="NIGHTFALL",
        weapon="emp",
        when="no_redsign",
        hour="super_early",
        targets="rival_probes",
        min_targets=2,
        combines_with="standalone",
        why=(
            "on a night with no pure lit, their vision IS their plan; one cloud "
            "over two or more clustered eyes blinds their whole read for eight "
            "hours and refuses the landings those eyes were covering"
        ),
    ),
    WeaponPlay(
        play_id="TEMPO_TAX",
        weapon="snap",
        when="always",
        hour="early",
        targets="rival_probes",
        min_targets=1,
        combines_with="standalone",
        why=(
            "killing the single freshest eye that lights their best target "
            "costs us 100 blue and costs them the landing it was covering; "
            "small and cheap, but it taxes their tempo every night we can afford it"
        ),
    ),
    # ─── ADD YOUR MOVE HERE ───────────────────────────────────────────────
    # Both examples below are COMMENTED OUT on purpose. Uncomment one and
    # rename it, or write your own. An unedited file declares NO plays and
    # `check_wiring.py` will say so — that is correct, not a bug.
    #
    # It used to ship CANCEL_SMASH live, and six separate builders either
    # shipped it by accident or spent time working out whether they should.

    # ─────────────────────────────────────────────────────────────────────
    # THIS IS A PLACEHOLDER. Rename `play_id` to YOUR move and rewrite `why`,
    # or delete the whole block. It is live code, not a comment: leave it and
    # your agent ships a move called CANCEL_SMASH, buys chaff to feed it, and
    # your own weapon competes with it on the menu.
    # ─────────────────────────────────────────────────────────────────────
    # WeaponPlay(
    #     play_id="CANCEL_SMASH",
    #     weapon="chaff",
    #     when="redsign_theirs",
    #     hour="super_early",
    #     combines_with="blind_grab",
    #     why=(
    #         "a seat that has just found a pure drops on it at hour 1, so "
    #         "cancelling that one hour takes their whole opening and leaves the "
    #         "pure sitting there for us to walk onto"
    #     ),
    # ),
    #
    # # Add more moves here. A second weapon is one more entry — for example:
    #
    # WeaponPlay(
    #     play_id="TEMPO_TAX",
    #     weapon="snap",
    #     when="always",
    #     hour="early",
    #     combines_with="standalone",
    #     why="killing the single eye that lights their best target costs us "
    #         "100 blue and costs them the landing it was covering",
    # ),
)
