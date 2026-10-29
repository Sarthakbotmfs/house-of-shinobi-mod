# -*- coding: utf-8 -*-
"""
House of Shinobi (HoS) - Comprehensive Shinobi MOD System & Menu
================================================================
Engine: Ren'Py 8.2 (Python 3.9)
Theme: Dark shinobi / ninja aesthetic (obsidian, purple, gold, crimson)
Resolution: 1280x720

Integrates seamlessly via game/python-packages/ without modifying any
hashed engine files or triggering _glcache.pyd integrity checks.
"""

import sys
import os

try:
    import renpy
    from renpy import store
except ImportError:
    renpy = None
    store = None


# ============================================================================
# 1. CORE MOD BACKEND LOGIC
# ============================================================================

ALL_SHOP_ITEMS = [
    ("camera", "Camera", 75),
    ("bikini", "Bikini", 100),
    ("blackdress", "Black Dress", 150),
    ("massagebooklvl1", "Massage Tips Volume 1", 50),
    ("blindfold", "Blindfold", 30),
    ("pool", "Pool installation", 400),
    ("swimsuit", "Swimsuit", 120),
    ("cosplayoutfitcammy", "Cammy Outfit", 200),
    ("cosplayoutfitchunli", "Chunli Outfit", 200),
    ("maidoutfit", "Maid Outfit", 200),
    ("cosplayoutfitslave", "Slave Outfit", 200),
    ("Lockpicks", "Lockpicks", 50),
]

DAY_NAMES = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
DAY_PART_NAMES = ("Morning", "Evening", "Night")


def safe_play_sfx(path="audio/soun_fx/attributes.opus"):
    """Play a sound effect safely without crashing if audio device unavailable."""
    if not renpy:
        return
    try:
        renpy.play(path, channel="sound")
    except Exception:
        pass


def safe_notify(message):
    """Display an in-game notification banner."""
    if not renpy:
        return
    try:
        renpy.notify("{color=#FFD700}[[MOD]]{/color} " + str(message))
    except Exception:
        pass


def safe_restart():
    """Trigger Ren'Py interaction update."""
    if not renpy:
        return
    try:
        renpy.restart_interaction()
    except Exception:
        pass


# --- Stat Helpers ---

def get_stat_obj(stat_name):
    """Retrieve a Stat instance from renpy.store."""
    if not renpy or not hasattr(renpy, "store"):
        return None
    return getattr(renpy.store, stat_name, None)


def get_stat_info(stat_name):
    """Return (value, level) for a stat safely."""
    obj = get_stat_obj(stat_name)
    if obj is not None:
        val = getattr(obj, "value", 0)
        lvl = getattr(obj, "level", 1)
        return int(val), int(lvl)
    return 0, 1


def change_stat(stat_name, delta):
    """Add or subtract from a stat using the game's official or safe method."""
    if not renpy or not hasattr(renpy, "store"):
        return
    st = renpy.store
    try:
        # Check if the game's official change_stat_in_place is available
        if hasattr(st, "change_stat_in_place") and callable(st.change_stat_in_place):
            st.change_stat_in_place(stat_name, delta)
        else:
            obj = getattr(st, stat_name, None)
            if obj is not None:
                new_v = max(0, getattr(obj, "value", 0) + delta)
                obj.value = new_v

        # Sync legacy corruption variables if applicable
        if stat_name == "hinata_corruption":
            obj = getattr(st, stat_name, None)
            if obj is not None:
                setattr(st, "server_tolerance", getattr(obj, "value", 0))
                setattr(st, "ramen_corruption_tier", getattr(obj, "level", 1))

        val, lvl = get_stat_info(stat_name)
        safe_play_sfx("audio/soun_fx/attributes.opus")
        safe_notify(f"{stat_name.replace('_', ' ').title()}: {val} (Lvl {lvl})")
        safe_restart()
    except Exception as e:
        safe_notify(f"Error modifying {stat_name}: {e}")


def set_stat(stat_name, new_value, new_level=None):
    """Set a stat directly to a specific value and optional level."""
    if not renpy or not hasattr(renpy, "store"):
        return
    st = renpy.store
    try:
        obj = getattr(st, stat_name, None)
        if obj is not None:
            obj.value = max(0, int(new_value))
            if new_level is not None:
                obj.level = max(1, int(new_level))

        if stat_name == "hinata_corruption":
            setattr(st, "server_tolerance", int(new_value))
            if new_level is not None:
                setattr(st, "ramen_corruption_tier", int(new_level))

        val, lvl = get_stat_info(stat_name)
        safe_play_sfx("audio/soun_fx/attributes.opus")
        safe_notify(f"{stat_name.replace('_', ' ').title()} set to {val} (Lvl {lvl})")
        safe_restart()
    except Exception as e:
        safe_notify(f"Error setting {stat_name}: {e}")


def max_all_character_stats():
    """Set all character stats to 100."""
    stats = [
        "dominance", "hatred", "hinata_love", "himawari_love",
        "hinata_obedience", "himawari_obedience", "hinata_corruption"
    ]
    for s in stats:
        set_stat(s, 100, 5)
    safe_play_sfx("audio/soun_fx/attributes.opus")
    safe_notify("All character stats maximized to 100!")


# --- Player Skills Helpers ---

def get_player_skill(name):
    """Get strengthlevel or massageknowledge."""
    if not renpy or not hasattr(renpy, "store"):
        return 0
    return int(getattr(renpy.store, name, 0))


def change_player_skill(name, delta, max_val=100):
    """Modify strengthlevel or massageknowledge."""
    if not renpy or not hasattr(renpy, "store"):
        return
    st = renpy.store
    curr = getattr(st, name, 0)
    new_v = max(0, min(max_val, curr + delta))
    setattr(st, name, new_v)
    safe_play_sfx("audio/soun_fx/attributes.opus")
    safe_notify(f"{name.title()}: {new_v}")
    safe_restart()


def set_player_skill(name, val):
    """Set strengthlevel or massageknowledge directly."""
    if not renpy or not hasattr(renpy, "store"):
        return
    setattr(renpy.store, name, int(val))
    safe_play_sfx("audio/soun_fx/attributes.opus")
    safe_notify(f"{name.title()} set to {val}")
    safe_restart()


def max_player_skills():
    """Max both strengthlevel (100) and massageknowledge (10)."""
    if not renpy or not hasattr(renpy, "store"):
        return
    setattr(renpy.store, "strengthlevel", 100)
    setattr(renpy.store, "massageknowledge", 10)
    safe_play_sfx("audio/soun_fx/attributes.opus")
    safe_notify("MC Strength (100) & Massage (10) Maximized!")
    safe_restart()


# --- Economy & Items Helpers ---

def get_cash():
    """Get player cash."""
    if not renpy or not hasattr(renpy, "store"):
        return 0
    return int(getattr(renpy.store, "availablemoneytobepaid", 0))


def add_cash(amount):
    """Add cash to player."""
    if not renpy or not hasattr(renpy, "store"):
        return
    st = renpy.store
    curr = getattr(st, "availablemoneytobepaid", 0)
    setattr(st, "availablemoneytobepaid", max(0, curr + amount))
    safe_play_sfx("audio/soun_fx/money2.opus")
    safe_notify(f"Cash updated: ¥{getattr(st, 'availablemoneytobepaid')}")
    safe_restart()


def set_cash(amount):
    """Set player cash."""
    if not renpy or not hasattr(renpy, "store"):
        return
    setattr(renpy.store, "availablemoneytobepaid", max(0, int(amount)))
    safe_play_sfx("audio/soun_fx/money2.opus")
    safe_notify(f"Cash set to ¥{int(amount)}")
    safe_restart()


def get_ramen():
    """Get ramen currency."""
    if not renpy or not hasattr(renpy, "store"):
        return 0
    return int(getattr(renpy.store, "ramencurrency", 0))


def add_ramen(amount):
    """Add ramen currency."""
    if not renpy or not hasattr(renpy, "store"):
        return
    st = renpy.store
    curr = getattr(st, "ramencurrency", 0)
    setattr(st, "ramencurrency", max(0, curr + amount))
    safe_play_sfx("audio/soun_fx/money2.opus")
    safe_notify(f"Ramen Currency updated: ¥{getattr(st, 'ramencurrency')}")
    safe_restart()


def set_ramen(amount):
    """Set ramen currency."""
    if not renpy or not hasattr(renpy, "store"):
        return
    setattr(renpy.store, "ramencurrency", max(0, int(amount)))
    safe_play_sfx("audio/soun_fx/money2.opus")
    safe_notify(f"Ramen Currency set to ¥{int(amount)}")
    safe_restart()


def get_item_quantity(item_name):
    """Get quantity of item in player's inventory."""
    if not renpy or not hasattr(renpy, "store"):
        return 0
    inv = getattr(renpy.store, "inventory", None)
    if not inv or not hasattr(inv, "items"):
        return 0
    for it in inv.items:
        if getattr(it, "name", None) == item_name:
            return getattr(it, "quantity", 1)
    return 0


def add_item_to_inventory(item_name, info="Shop Item", price=50, quantity=1):
    """Safely create and add an item to the player's inventory."""
    if not renpy or not hasattr(renpy, "store"):
        return
    st = renpy.store
    inv = getattr(st, "inventory", None)
    item_cls = getattr(st, "Item", None)
    if not inv or not item_cls:
        safe_notify("Inventory system not yet initialized in current save.")
        return

    existing = None
    if hasattr(inv, "find_item_by_name"):
        existing = inv.find_item_by_name(item_name)

    if existing is not None:
        existing.quantity = getattr(existing, "quantity", 0) + quantity
    else:
        new_item = item_cls(item_name, info, price, quantity)
        if hasattr(inv, "add_item"):
            inv.add_item(new_item, quantity)
        elif hasattr(inv, "items"):
            inv.items.append(new_item)

    # Track in unique shop purchases
    purchased = getattr(st, "shop_purchased_unique_items", None)
    if purchased is not None:
        if isinstance(purchased, set):
            purchased.add(item_name)
        elif isinstance(purchased, list) and item_name not in purchased:
            purchased.append(item_name)

    safe_play_sfx("audio/soun_fx/attributes.opus")
    safe_notify(f"Added item: {info}")
    safe_restart()


def add_all_shop_items():
    """Add all 12 key outfits and shop items to player inventory."""
    for item_name, info, price in ALL_SHOP_ITEMS:
        add_item_to_inventory(item_name, info, price, 1)
    safe_play_sfx("audio/soun_fx/attributes.opus")
    safe_notify("All 12 Outfits and Key Items added to Inventory!")
    safe_restart()


# --- Time & Calendar Helpers ---

def get_day_info():
    """Return (day_number, day_name, day_part, day_part_name)."""
    if not renpy or not hasattr(renpy, "store"):
        return 0, "Monday", 0, "Morning"
    st = renpy.store
    dn = getattr(st, "day_number", 0)
    dp = getattr(st, "day_part", 0)
    dname = getattr(st, "day_name", DAY_NAMES[dn % 7])
    dpname = getattr(st, "day_part_name", DAY_PART_NAMES[dp % 3])
    return dn, dname, dp, dpname


def set_time(day_number=None, day_part=None):
    """Set calendar day and/or day part safely."""
    if not renpy or not hasattr(renpy, "store"):
        return
    st = renpy.store
    if day_number is not None:
        st.day_number = max(0, int(day_number))
        st.day_name = DAY_NAMES[st.day_number % 7]
    if day_part is not None:
        st.day_part = int(day_part) % 3
        st.day_part_name = DAY_PART_NAMES[st.day_part]

    dn, dname, dp, dpname = get_day_info()
    safe_play_sfx("audio/soun_fx/attributes.opus")
    safe_notify(f"Time set to: Day {dn} ({dname}), {dpname}")
    safe_restart()


def advance_day_part():
    """Advance to the next period of the day (Morning -> Evening -> Night -> Next Day)."""
    if not renpy or not hasattr(renpy, "store"):
        return
    st = renpy.store
    dp = getattr(st, "day_part", 0) + 1
    if dp >= 3:
        st.day_part = 0
        st.day_number = getattr(st, "day_number", 0) + 1
        st.day_name = DAY_NAMES[st.day_number % 7]
    else:
        st.day_part = dp
    st.day_part_name = DAY_PART_NAMES[st.day_part]

    dn, dname, dp, dpname = get_day_info()
    safe_play_sfx("audio/soun_fx/attributes.opus")
    safe_notify(f"Advanced Time: Day {dn} ({dname}), {dpname}")
    safe_restart()


def change_day(delta):
    """Advance or rewind day count."""
    if not renpy or not hasattr(renpy, "store"):
        return
    st = renpy.store
    new_d = max(0, getattr(st, "day_number", 0) + delta)
    set_time(day_number=new_d)


# --- Master Unlocks ---

def unlock_all_gallery():
    """Unlock all 4,515 gallery images and animations."""
    if not renpy:
        return
    p = renpy.game.persistent
    st = renpy.store

    p.gallery_unlocker = True
    setattr(st, "gallery_unlocker", True)

    # Populate unlocked_gallery_items
    gallery_items = getattr(st, "gallery_items", [])
    if hasattr(p, "unlocked_gallery_items"):
        if p.unlocked_gallery_items is None:
            p.unlocked_gallery_items = []
        for g in gallery_items:
            dname = getattr(g, "display_name", None) or getattr(g, "name", None)
            if dname and dname not in p.unlocked_gallery_items:
                p.unlocked_gallery_items.append(dname)

    # Unlock in-memory objects
    for g in gallery_items:
        setattr(g, "_lk", False)

    try:
        renpy.save_persistent()
    except Exception:
        pass

    safe_play_sfx("audio/soun_fx/attributes.opus")
    safe_notify(f"Gallery Unlocked: {len(gallery_items)} CGs and animations!")
    safe_restart()


def unlock_all_replays():
    """Unlock all 765 scene replays."""
    if not renpy:
        return
    p = renpy.game.persistent
    st = renpy.store

    p.replay_unlocker = True
    setattr(st, "replay_unlocker", True)

    replay_items = getattr(st, "Replay_items", [])
    if hasattr(p, "unlocked_replay_items"):
        if p.unlocked_replay_items is None:
            p.unlocked_replay_items = []
        for r in replay_items:
            rname = getattr(r, "name", None)
            if rname and rname not in p.unlocked_replay_items:
                p.unlocked_replay_items.append(rname)

    try:
        renpy.save_persistent()
    except Exception:
        pass

    safe_play_sfx("audio/soun_fx/attributes.opus")
    safe_notify(f"Replays Unlocked: {len(replay_items)} scenes!")
    safe_restart()


def unlock_patron_and_bonuses():
    """Activate Patron Tier 3, Itch version, and bonus content."""
    if not renpy:
        return
    p = renpy.game.persistent
    st = renpy.store

    p.activated = True
    p.activation_tier = "PATREON"
    p.current_activation = "Tier 3"
    p.i_version = True
    p.itchset = True
    p.animations_enabled = True
    p.translationstring = getattr(p, "translationstring", 101218) + 1

    try:
        renpy.save_persistent()
    except Exception:
        pass

    safe_play_sfx("audio/soun_fx/attributes.opus")
    safe_notify("Patron Tier 3 & Supporter Content Activated!")
    safe_restart()


def unlock_all_quests():
    """Unlock pending quests across Boruto, Hinata, and Himawari managers."""
    if not renpy or not hasattr(renpy, "store"):
        return
    st = renpy.store
    count = 0
    for mgr_name in ("quest", "quest_hin", "quest_him"):
        mgr = getattr(st, mgr_name, None)
        if mgr and hasattr(mgr, "quests_dict") and mgr.quests_dict:
            for cat in mgr.quests_dict.values():
                for q in cat.values():
                    if getattr(q, "state", None) == "pending":
                        q.state = "unlocked"
                        count += 1
    safe_play_sfx("audio/soun_fx/attributes.opus")
    safe_notify(f"Unlocked {count} pending quests!")
    safe_restart()


def complete_all_quests():
    """Mark all quests completed across Boruto, Hinata, and Himawari managers."""
    if not renpy or not hasattr(renpy, "store"):
        return
    st = renpy.store
    count = 0
    for mgr_name in ("quest", "quest_hin", "quest_him"):
        mgr = getattr(st, mgr_name, None)
        if mgr and hasattr(mgr, "quests_dict") and mgr.quests_dict:
            for cat in mgr.quests_dict.values():
                for q in cat.values():
                    q.state = "completed"
                    count += 1
    safe_play_sfx("audio/soun_fx/attributes.opus")
    safe_notify(f"Completed {count} quests!")
    safe_restart()


def unlock_all_everything():
    """Master one-click unlock: Gallery, Replays, Patron, Outfits, Money."""
    unlock_all_gallery()
    unlock_all_replays()
    unlock_patron_and_bonuses()
    add_all_shop_items()
    add_cash(50000)
    add_ramen(20000)
    max_player_skills()
    safe_play_sfx("audio/soun_fx/attributes.opus")
    safe_notify("MASTER UNLOCK COMPLETE! All CGs, Replays, Patron content & Items unlocked!")
    safe_restart()


# ============================================================================
# 2. REN'PY SCREEN DEFINITIONS (Compiled in memory)
# ============================================================================

RENPY_MOD_SCREENS = r"""
init -490 python:
    import hos_mod

screen hos_mod_overlay():
    zorder 150
    key "K_F8" action ToggleScreen("hos_mod_menu")
    key "K_BACKQUOTE" action ToggleScreen("hos_mod_menu")

    frame:
        align (0.985, 0.02)
        background "#1a0b2ee0"
        padding (8, 4)
        has hbox:
            spacing 4
        textbutton "{color=#FFD700}⚡ MOD{/color}":
            text_size 14
            text_bold True
            text_hover_color "#E1BEE7"
            action ToggleScreen("hos_mod_menu")


screen hos_mod_menu():
    modal True
    zorder 200

    default current_tab = "stats"

    # Dark backdrop
    add "#06060de6"

    # Close on Escape or F8
    key "K_ESCAPE" action Hide("hos_mod_menu")
    key "K_F8" action Hide("hos_mod_menu")
    key "K_BACKQUOTE" action Hide("hos_mod_menu")

    # Main Window Frame
    frame:
        align (0.5, 0.5)
        xysize (1180, 660)
        background "#111018"
        padding (16, 14)

        has vbox:
            spacing 10

        # --- Top Header ---
        hbox:
            xfill True
            spacing 10

            vbox:
                spacing 2
                text "{color=#FFD700}★ SHINOBI MOD MENU ★{/color}  {color=#CE93D8}House of Shinobi v0.26d{/color}":
                    size 22
                    bold True
                $ d_num, d_name, d_part, d_part_name = hos_mod.get_day_info()
                $ p_cash = hos_mod.get_cash()
                $ p_ramen = hos_mod.get_ramen()
                text ("{color=#9E9E9E}Day: {color=#FFFFFF}%d (%s, %s){/color}  |  Cash: {color=#81C784}¥%d{/color}  |  Ramen: {color=#FFB74D}¥%d{/color}{/color}" % (d_num, d_name, d_part_name, p_cash, p_ramen)):
                    size 13

            textbutton "{color=#FF5252}✕ CLOSE{/color}":
                align (1.0, 0.2)
                text_size 15
                text_bold True
                text_hover_color "#FF8A80"
                action Hide("hos_mod_menu")

        # Subtle separator
        frame:
            xfill True
            ysize 2
            background "#4A148C"

        # --- Tabs Bar ---
        hbox:
            spacing 6

            textbutton "{color=#FFFFFF}📊 STATS{/color}":
                text_size 14
                text_bold (current_tab == "stats")
                background ("#6A1B9A" if current_tab == "stats" else "#1F1B2E")
                padding (12, 6)
                action SetScreenVariable("current_tab", "stats")

            textbutton "{color=#FFFFFF}⚡ MC & SKILLS{/color}":
                text_size 14
                text_bold (current_tab == "skills")
                background ("#6A1B9A" if current_tab == "skills" else "#1F1B2E")
                padding (12, 6)
                action SetScreenVariable("current_tab", "skills")

            textbutton "{color=#FFFFFF}💰 ECONOMY & ITEMS{/color}":
                text_size 14
                text_bold (current_tab == "economy")
                background ("#6A1B9A" if current_tab == "economy" else "#1F1B2E")
                padding (12, 6)
                action SetScreenVariable("current_tab", "economy")

            textbutton "{color=#FFFFFF}⏳ CALENDAR & TIME{/color}":
                text_size 14
                text_bold (current_tab == "time")
                background ("#6A1B9A" if current_tab == "time" else "#1F1B2E")
                padding (12, 6)
                action SetScreenVariable("current_tab", "time")

            textbutton "{color=#FFD700}🔓 MASTER UNLOCKS{/color}":
                text_size 14
                text_bold (current_tab == "unlocks")
                background ("#6A1B9A" if current_tab == "unlocks" else "#1F1B2E")
                padding (12, 6)
                action SetScreenVariable("current_tab", "unlocks")

            textbutton "{color=#FFFFFF}📜 QUESTS{/color}":
                text_size 14
                text_bold (current_tab == "quests")
                background ("#6A1B9A" if current_tab == "quests" else "#1F1B2E")
                padding (12, 6)
                action SetScreenVariable("current_tab", "quests")

        # --- Main Tab Content Area ---
        viewport:
            xfill True
            ysize 470
            scrollbars "vertical"
            mousewheel True
            draggable True

            vbox:
                spacing 12

                # ========================================================
                # TAB 1: CHARACTER STATS
                # ========================================================
                if current_tab == "stats":
                    hbox:
                        spacing 15
                        text "{color=#CE93D8}{b}CHARACTER RELATIONSHIP & PATH STATS{/b}{/color}":
                            size 16
                            align (0.0, 0.5)

                        textbutton "{color=#FFD700}⚡ Max All Character Stats (100){/color}":
                            text_size 13
                            background "#3E1E5C"
                            padding (8, 4)
                            action Function(hos_mod.max_all_character_stats)

                    # Hinata Stats Card
                    frame:
                        xfill True
                        background "#191526"
                        padding (12, 10)
                        has vbox:
                            spacing 8
                        text "{color=#CE93D8}{b}HINATA{/b}{/color}":
                            size 15

                        # Hinata Love
                        $ h_love_val, h_love_lvl = hos_mod.get_stat_info("hinata_love")
                        hbox:
                            spacing 10
                            text ("{color=#F06292}Hinata Love:{/color}  Val: {b}%d{/b} | Lvl: {b}%d{/b}" % (h_love_val, h_love_lvl)):
                                size 14
                                xsize 250
                                align (0.0, 0.5)
                            textbutton "-10" text_size 12 background "#2A1838" padding (8, 3) action Function(hos_mod.change_stat, "hinata_love", -10)
                            textbutton "-1" text_size 12 background "#2A1838" padding (8, 3) action Function(hos_mod.change_stat, "hinata_love", -1)
                            textbutton "+1" text_size 12 background "#2A1838" padding (8, 3) action Function(hos_mod.change_stat, "hinata_love", 1)
                            textbutton "+10" text_size 12 background "#2A1838" padding (8, 3) action Function(hos_mod.change_stat, "hinata_love", 10)
                            textbutton "MAX (100)" text_size 12 background "#4A148C" padding (8, 3) action Function(hos_mod.set_stat, "hinata_love", 100, 5)

                        # Hinata Obedience
                        $ h_obe_val, h_obe_lvl = hos_mod.get_stat_info("hinata_obedience")
                        hbox:
                            spacing 10
                            text ("{color=#BA68C8}Hinata Obedience:{/color}  Val: {b}%d{/b} | Lvl: {b}%d{/b}" % (h_obe_val, h_obe_lvl)):
                                size 14
                                xsize 250
                                align (0.0, 0.5)
                            textbutton "-10" text_size 12 background "#2A1838" padding (8, 3) action Function(hos_mod.change_stat, "hinata_obedience", -10)
                            textbutton "-1" text_size 12 background "#2A1838" padding (8, 3) action Function(hos_mod.change_stat, "hinata_obedience", -1)
                            textbutton "+1" text_size 12 background "#2A1838" padding (8, 3) action Function(hos_mod.change_stat, "hinata_obedience", 1)
                            textbutton "+10" text_size 12 background "#2A1838" padding (8, 3) action Function(hos_mod.change_stat, "hinata_obedience", 10)
                            textbutton "MAX (100)" text_size 12 background "#4A148C" padding (8, 3) action Function(hos_mod.set_stat, "hinata_obedience", 100, 5)

                        # Hinata Corruption
                        $ h_cor_val, h_cor_lvl = hos_mod.get_stat_info("hinata_corruption")
                        hbox:
                            spacing 10
                            text ("{color=#9575CD}Hinata Corruption:{/color}  Val: {b}%d{/b} | Lvl: {b}%d{/b}" % (h_cor_val, h_cor_lvl)):
                                size 14
                                xsize 250
                                align (0.0, 0.5)
                            textbutton "-10" text_size 12 background "#2A1838" padding (8, 3) action Function(hos_mod.change_stat, "hinata_corruption", -10)
                            textbutton "-1" text_size 12 background "#2A1838" padding (8, 3) action Function(hos_mod.change_stat, "hinata_corruption", -1)
                            textbutton "+1" text_size 12 background "#2A1838" padding (8, 3) action Function(hos_mod.change_stat, "hinata_corruption", 1)
                            textbutton "+10" text_size 12 background "#2A1838" padding (8, 3) action Function(hos_mod.change_stat, "hinata_corruption", 10)
                            textbutton "MAX (100)" text_size 12 background "#4A148C" padding (8, 3) action Function(hos_mod.set_stat, "hinata_corruption", 100, 5)

                    # Himawari Stats Card
                    frame:
                        xfill True
                        background "#161c29"
                        padding (12, 10)
                        has vbox:
                            spacing 8
                        text "{color=#64B5F6}{b}HIMAWARI{/b}{/color}":
                            size 15

                        # Himawari Love
                        $ him_love_val, him_love_lvl = hos_mod.get_stat_info("himawari_love")
                        hbox:
                            spacing 10
                            text ("{color=#64B5F6}Himawari Love:{/color}  Val: {b}%d{/b} | Lvl: {b}%d{/b}" % (him_love_val, him_love_lvl)):
                                size 14
                                xsize 250
                                align (0.0, 0.5)
                            textbutton "-10" text_size 12 background "#14253B" padding (8, 3) action Function(hos_mod.change_stat, "himawari_love", -10)
                            textbutton "-1" text_size 12 background "#14253B" padding (8, 3) action Function(hos_mod.change_stat, "himawari_love", -1)
                            textbutton "+1" text_size 12 background "#14253B" padding (8, 3) action Function(hos_mod.change_stat, "himawari_love", 1)
                            textbutton "+10" text_size 12 background "#14253B" padding (8, 3) action Function(hos_mod.change_stat, "himawari_love", 10)
                            textbutton "MAX (100)" text_size 12 background "#1565C0" padding (8, 3) action Function(hos_mod.set_stat, "himawari_love", 100, 5)

                        # Himawari Obedience
                        $ him_obe_val, him_obe_lvl = hos_mod.get_stat_info("himawari_obedience")
                        hbox:
                            spacing 10
                            text ("{color=#4DD0E1}Himawari Obedience:{/color}  Val: {b}%d{/b} | Lvl: {b}%d{/b}" % (him_obe_val, him_obe_lvl)):
                                size 14
                                xsize 250
                                align (0.0, 0.5)
                            textbutton "-10" text_size 12 background "#14253B" padding (8, 3) action Function(hos_mod.change_stat, "himawari_obedience", -10)
                            textbutton "-1" text_size 12 background "#14253B" padding (8, 3) action Function(hos_mod.change_stat, "himawari_obedience", -1)
                            textbutton "+1" text_size 12 background "#14253B" padding (8, 3) action Function(hos_mod.change_stat, "himawari_obedience", 1)
                            textbutton "+10" text_size 12 background "#14253B" padding (8, 3) action Function(hos_mod.change_stat, "himawari_obedience", 10)
                            textbutton "MAX (100)" text_size 12 background "#1565C0" padding (8, 3) action Function(hos_mod.set_stat, "himawari_obedience", 100, 5)

                    # MC Dominance & Hatred Card
                    frame:
                        xfill True
                        background "#261919"
                        padding (12, 10)
                        has vbox:
                            spacing 8
                        text "{color=#FFD54F}{b}MAIN CHARACTER (BORUTO){/b}{/color}":
                            size 15

                        # Dominance
                        $ dom_val, dom_lvl = hos_mod.get_stat_info("dominance")
                        hbox:
                            spacing 10
                            text ("{color=#FFD54F}Dominance:{/color}  Val: {b}%d{/b} | Lvl: {b}%d{/b}" % (dom_val, dom_lvl)):
                                size 14
                                xsize 250
                                align (0.0, 0.5)
                            textbutton "-10" text_size 12 background "#3B2614" padding (8, 3) action Function(hos_mod.change_stat, "dominance", -10)
                            textbutton "-1" text_size 12 background "#3B2614" padding (8, 3) action Function(hos_mod.change_stat, "dominance", -1)
                            textbutton "+1" text_size 12 background "#3B2614" padding (8, 3) action Function(hos_mod.change_stat, "dominance", 1)
                            textbutton "+10" text_size 12 background "#3B2614" padding (8, 3) action Function(hos_mod.change_stat, "dominance", 10)
                            textbutton "MAX (100)" text_size 12 background "#F57F17" padding (8, 3) action Function(hos_mod.set_stat, "dominance", 100, 5)

                        # Hatred
                        $ hat_val, hat_lvl = hos_mod.get_stat_info("hatred")
                        hbox:
                            spacing 10
                            text ("{color=#E57373}Hatred:{/color}  Val: {b}%d{/b} | Lvl: {b}%d{/b}" % (hat_val, hat_lvl)):
                                size 14
                                xsize 250
                                align (0.0, 0.5)
                            textbutton "-10" text_size 12 background "#3B1414" padding (8, 3) action Function(hos_mod.change_stat, "hatred", -10)
                            textbutton "-1" text_size 12 background "#3B1414" padding (8, 3) action Function(hos_mod.change_stat, "hatred", -1)
                            textbutton "+1" text_size 12 background "#3B1414" padding (8, 3) action Function(hos_mod.change_stat, "hatred", 1)
                            textbutton "+10" text_size 12 background "#3B1414" padding (8, 3) action Function(hos_mod.change_stat, "hatred", 10)
                            textbutton "MAX (100)" text_size 12 background "#C62828" padding (8, 3) action Function(hos_mod.set_stat, "hatred", 100, 5)


                # ========================================================
                # TAB 2: MC SKILLS & PHYSICAL
                # ========================================================
                elif current_tab == "skills":
                    text "{color=#CE93D8}{b}MC PHYSICAL & PROFESSIONAL SKILLS{/b}{/color}":
                        size 16

                    frame:
                        xfill True
                        background "#191526"
                        padding (14, 12)
                        has vbox:
                            spacing 12

                        # Strength Level
                        $ s_lvl = hos_mod.get_player_skill("strengthlevel")
                        hbox:
                            spacing 10
                            text ("{color=#FF8A65}Physical Strength Level:{/color}  {b}%d / 100{/b}" % s_lvl):
                                size 15
                                xsize 300
                                align (0.0, 0.5)
                            textbutton "-10" text_size 13 background "#2A1838" padding (10, 4) action Function(hos_mod.change_player_skill, "strengthlevel", -10, 100)
                            textbutton "-5" text_size 13 background "#2A1838" padding (10, 4) action Function(hos_mod.change_player_skill, "strengthlevel", -5, 100)
                            textbutton "+5" text_size 13 background "#2A1838" padding (10, 4) action Function(hos_mod.change_player_skill, "strengthlevel", 5, 100)
                            textbutton "+10" text_size 13 background "#2A1838" padding (10, 4) action Function(hos_mod.change_player_skill, "strengthlevel", 10, 100)
                            textbutton "{color=#FFD700}SET MAX (100){/color}" text_size 13 background "#4A148C" padding (10, 4) action Function(hos_mod.set_player_skill, "strengthlevel", 100)

                        # Massage Knowledge
                        $ m_lvl = hos_mod.get_player_skill("massageknowledge")
                        hbox:
                            spacing 10
                            text ("{color=#4DB6AC}Massage Technique Level:{/color}  {b}%d / 10{/b}" % m_lvl):
                                size 15
                                xsize 300
                                align (0.0, 0.5)
                            textbutton "-1" text_size 13 background "#2A1838" padding (10, 4) action Function(hos_mod.change_player_skill, "massageknowledge", -1, 10)
                            textbutton "+1" text_size 13 background "#2A1838" padding (10, 4) action Function(hos_mod.change_player_skill, "massageknowledge", 1, 10)
                            textbutton "{color=#FFD700}SET MAX (10){/color}" text_size 13 background "#4A148C" padding (10, 4) action Function(hos_mod.set_player_skill, "massageknowledge", 10)

                        frame:
                            xfill True
                            ysize 1
                            background "#332244"

                        textbutton "{color=#FFD700}⚡ Max Both Skills Instantly{/color}":
                            text_size 14
                            background "#4A148C"
                            padding (12, 6)
                            action Function(hos_mod.max_player_skills)


                # ========================================================
                # TAB 3: ECONOMY & INVENTORY
                # ========================================================
                elif current_tab == "economy":
                    text "{color=#CE93D8}{b}CURRENCY & INVENTORY MANAGEMENT{/b}{/color}":
                        size 16

                    # Currency Frame
                    frame:
                        xfill True
                        background "#191526"
                        padding (14, 12)
                        has vbox:
                            spacing 10

                        # Cash
                        $ p_c = hos_mod.get_cash()
                        hbox:
                            spacing 10
                            text ("{color=#81C784}Player Cash:{/color}  {b}¥%d{/b}" % p_c):
                                size 15
                                xsize 240
                                align (0.0, 0.5)
                            textbutton "+¥1,000" text_size 12 background "#1B3B22" padding (8, 4) action Function(hos_mod.add_cash, 1000)
                            textbutton "+¥10,000" text_size 12 background "#1B3B22" padding (8, 4) action Function(hos_mod.add_cash, 10000)
                            textbutton "+¥50,000" text_size 12 background "#1B3B22" padding (8, 4) action Function(hos_mod.add_cash, 50000)
                            textbutton "{color=#FFD700}¥999,999{/color}" text_size 12 background "#4A148C" padding (8, 4) action Function(hos_mod.set_cash, 999999)
                            textbutton "Reset (1k)" text_size 12 background "#3B1B1B" padding (8, 4) action Function(hos_mod.set_cash, 1000)

                        # Ramen Currency
                        $ p_r = hos_mod.get_ramen()
                        hbox:
                            spacing 10
                            text ("{color=#FFB74D}Ramen Tavern Cash:{/color}  {b}¥%d{/b}" % p_r):
                                size 15
                                xsize 240
                                align (0.0, 0.5)
                            textbutton "+¥500" text_size 12 background "#3B2E1B" padding (8, 4) action Function(hos_mod.add_ramen, 500)
                            textbutton "+¥2,000" text_size 12 background "#3B2E1B" padding (8, 4) action Function(hos_mod.add_ramen, 2000)
                            textbutton "+¥10,000" text_size 12 background "#3B2E1B" padding (8, 4) action Function(hos_mod.add_ramen, 10000)
                            textbutton "{color=#FFD700}¥50,000{/color}" text_size 12 background "#4A148C" padding (8, 4) action Function(hos_mod.set_ramen, 50000)

                    # Outfits & Items Section
                    frame:
                        xfill True
                        background "#161924"
                        padding (14, 12)
                        has vbox:
                            spacing 10

                        hbox:
                            spacing 15
                            text "{color=#CE93D8}{b}SHOP ITEMS & OUTFITS{/b}{/color}":
                                size 15
                                align (0.0, 0.5)

                            textbutton "{color=#FFD700}🎁 Add ALL 12 Outfits & Shop Items{/color}":
                                text_size 13
                                background "#4A148C"
                                padding (10, 4)
                                action Function(hos_mod.add_all_shop_items)

                        grid 3 4:
                            xfill True
                            spacing 8
                            for item_key, item_title, item_price in hos_mod.ALL_SHOP_ITEMS:
                                $ q = hos_mod.get_item_quantity(item_key)
                                frame:
                                    background "#1e1e2d"
                                    padding (8, 6)
                                    has hbox:
                                        spacing 6
                                    vbox:
                                        xsize 220
                                        text ("%s" % item_title) size 13 bold True color "#FFFFFF"
                                        text ("In bag: %d" % q) size 11 color ("#81C784" if q > 0 else "#757575")
                                    textbutton ("+1" if q > 0 else "Unlock") text_size 11 background "#3E1E5C" padding (6, 3) action Function(hos_mod.add_item_to_inventory, item_key, item_title, item_price, 1)


                # ========================================================
                # TAB 4: CALENDAR & TIME
                # ========================================================
                elif current_tab == "time":
                    text "{color=#CE93D8}{b}CALENDAR & TIME OF DAY CONTROLS{/b}{/color}":
                        size 16

                    frame:
                        xfill True
                        background "#191526"
                        padding (14, 12)
                        has vbox:
                            spacing 12

                        $ cur_dn, cur_dname, cur_dp, cur_dpname = hos_mod.get_day_info()
                        text ("Current Date & Time: {color=#FFD700}Day %d (%s){/color} — {color=#CE93D8}%s{/color} (Period %d)" % (cur_dn, cur_dname, cur_dpname, cur_dp)):
                            size 16

                        # Time of Day Jump
                        vbox:
                            spacing 6
                            text "{color=#E0E0E0}Set Time of Day:{/color}" size 14
                            hbox:
                                spacing 8
                                textbutton "🌅 Morning (0)" text_size 13 background ("#4A148C" if cur_dp == 0 else "#221A33") padding (12, 6) action Function(hos_mod.set_time, day_part=0)
                                textbutton "🌆 Evening (1)" text_size 13 background ("#4A148C" if cur_dp == 1 else "#221A33") padding (12, 6) action Function(hos_mod.set_time, day_part=1)
                                textbutton "🌙 Night (2)" text_size 13 background ("#4A148C" if cur_dp == 2 else "#221A33") padding (12, 6) action Function(hos_mod.set_time, day_part=2)
                                textbutton "⏩ Advance +1 Period" text_size 13 background "#1F3A52" padding (12, 6) action Function(hos_mod.advance_day_part)

                        frame:
                            xfill True
                            ysize 1
                            background "#332244"

                        # Day Counter Jump
                        vbox:
                            spacing 6
                            text "{color=#E0E0E0}Modify Day Counter:{/color}" size 14
                            hbox:
                                spacing 8
                                textbutton "⏪ -1 Day" text_size 12 background "#2A1838" padding (10, 5) action Function(hos_mod.change_day, -1)
                                textbutton "📅 +1 Day" text_size 12 background "#2A1838" padding (10, 5) action Function(hos_mod.change_day, 1)
                                textbutton "⏩ +5 Days" text_size 12 background "#2A1838" padding (10, 5) action Function(hos_mod.change_day, 5)

                            hbox:
                                spacing 6
                                text "Jump to Day:" size 13 color "#AAAAAA" align (0.0, 0.5)
                                for target_d in (1, 5, 10, 15, 20, 25, 30):
                                    textbutton ("Day %d" % target_d) text_size 12 background ("#4A148C" if cur_dn == target_d else "#1F1B2E") padding (8, 4) action Function(hos_mod.set_time, day_number=target_d)


                # ========================================================
                # TAB 5: MASTER UNLOCKS
                # ========================================================
                elif current_tab == "unlocks":
                    text "{color=#FFD700}{b}★ MASTER UNLOCK SYSTEM ★{/b}{/color}":
                        size 17

                    # Hero One-Click Card
                    frame:
                        xfill True
                        background "#2B1042"
                        padding (16, 14)
                        has vbox:
                            spacing 8
                        text "{color=#FFD700}{b}🌟 ONE-CLICK COMPLETE UNLOCK{/b}{/color}":
                            size 16
                        text "Unlocks all 4,515 Gallery CGs/Animations, 765 Scene Replays, full Patron Tier 3 status, itch mode, adds all 12 items/outfits, ¥50k Cash, ¥20k Ramen, and maxes player skills.":
                            size 13
                            color "#E1BEE7"
                        textbutton "{color=#FFD700}⚡ UNLOCK EVERYTHING NOW ⚡{/color}":
                            text_size 15
                            text_bold True
                            background "#6A1B9A"
                            padding (16, 8)
                            action Function(hos_mod.unlock_all_everything)

                    # Individual Unlock Cards
                    grid 2 2:
                        xfill True
                        spacing 10

                        frame:
                            background "#191526"
                            padding (12, 10)
                            has vbox:
                                spacing 6
                            text "{color=#CE93D8}{b}🖼️ CG Gallery{/b}{/color}":
                                size 14
                            text "Unlocks all 4,515 gallery illustrations, event CGs, and animations in the extras menu.":
                                size 12
                                color "#B0BEC5"
                            textbutton "Unlock Gallery (All CGs)" text_size 12 background "#4A148C" padding (8, 4) action Function(hos_mod.unlock_all_gallery)

                        frame:
                            background "#191526"
                            padding (12, 10)
                            has vbox:
                                spacing 6
                            text "{color=#CE93D8}{b}🎬 Scene Replays{/b}{/color}":
                                size 14
                            text "Unlocks all 765 interactive and erotic scene replays in the replay gallery.":
                                size 12
                                color "#B0BEC5"
                            textbutton "Unlock All Replays" text_size 12 background "#4A148C" padding (8, 4) action Function(hos_mod.unlock_all_replays)

                        frame:
                            background "#191526"
                            padding (12, 10)
                            has vbox:
                                spacing 6
                            text "{color=#FFD700}{b}👑 Patron & Supporter Tier 3{/b}{/color}":
                                size 14
                            text "Activates top Patreon tier verification, unlocks all subscriber-exclusive paths and animations.":
                                size 12
                                color "#B0BEC5"
                            textbutton "Activate Patron Tier 3" text_size 12 background "#6A1B9A" padding (8, 4) action Function(hos_mod.unlock_patron_and_bonuses)

                        frame:
                            background "#191526"
                            padding (12, 10)
                            has vbox:
                                spacing 6
                            text "{color=#81C784}{b}👗 Outfits & Key Items{/b}{/color}":
                                size 14
                            text "Adds Bikini, Swimsuit, Black Dress, Cammy, Chun-Li, Maid, Slave outfits, Camera, Pool to inventory.":
                                size 12
                                color "#B0BEC5"
                            textbutton "Add All 12 Items" text_size 12 background "#1B3B22" padding (8, 4) action Function(hos_mod.add_all_shop_items)


                # ========================================================
                # TAB 6: QUESTS & INTERACTIVE GUIDE
                # ========================================================
                elif current_tab == "quests":
                    text "{color=#CE93D8}{b}QUESTS & JOURNAL CONTROLS{/b}{/color}":
                        size 16

                    frame:
                        xfill True
                        background "#191526"
                        padding (14, 12)
                        has vbox:
                            spacing 12

                        text "Controls all journal quests across Boruto (MC), Hinata, and Himawari managers:":
                            size 13
                            color "#B0BEC5"

                        hbox:
                            spacing 12
                            textbutton "{color=#81C784}🔓 Unlock All Pending Quests{/color}":
                                text_size 13
                                background "#1B3B22"
                                padding (12, 6)
                                action Function(hos_mod.unlock_all_quests)

                            textbutton "{color=#FFD700}✅ Complete All Quests{/color}":
                                text_size 13
                                background "#4A148C"
                                padding (12, 6)
                                action Function(hos_mod.complete_all_quests)

        # --- Bottom Footer ---
        hbox:
            align (0.5, 0.5)
            text "Hotkeys: Press F8 or ~ (backtick) anytime during gameplay to toggle this MOD menu." size 12 color "#888899" substitute False
"""


# ============================================================================
# 3. MOD SYSTEM INSTALLATION & INJECTION
# ============================================================================

_mod_installed = False

def install_mod():
    """Compiles the mod screens into Ren'Py's in-memory AST and attaches overlay."""
    global _mod_installed
    if _mod_installed:
        return

    if not renpy or not hasattr(renpy, "game") or not hasattr(renpy.game, "script"):
        return

    script = renpy.game.script
    try:
        # Load and parse screen code into in-memory AST
        result = script.load_string("hos_mod_v2.rpy", RENPY_MOD_SCREENS)
        if result == (None, None):
            print("[HoS-MOD] Screen compilation error:")
            if hasattr(renpy.parser, 'parse_errors'):
                for err in renpy.parser.parse_errors:
                    print("  ", err)
            return
        stmts, initcode = result
        if initcode:
            for prio, node in initcode:
                node.execute()

        # Ensure the overlay is registered in always_shown_screens
        if hasattr(renpy.config, "always_shown_screens"):
            if "hos_mod_overlay" not in renpy.config.always_shown_screens:
                renpy.config.always_shown_screens.append("hos_mod_overlay")

        _mod_installed = True
        print("[HoS-MOD] Shinobi MOD Menu successfully initialized & registered!")
    except Exception as e:
        import traceback
        print(f"[HoS-MOD] Error during screen compilation: {e}")
        traceback.print_exc()
