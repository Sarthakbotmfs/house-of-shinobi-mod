# ★ House of Shinobi — Shinobi MOD Menu ★

A comprehensive, production-grade MOD system & interactive menu for **House of Shinobi (HoS v0.26d+)**.

Designed specifically in the game's dark ninja aesthetic with zero engine tampering, 100% save-compatibility, and anti-tamper DRM safety.

---

## 🌟 Key Features

### 🔓 1. Master Unlocks
* **🌟 One-Click Master Unlock**: Instantly unlocks all **4,515 CGs & Animations**, all **765 Scene Replays**, activates full **Patron Tier 3 status**, adds all 12 outfits & shop items, grants ¥50k Cash, ¥20k Ramen, and maxes MC skills.
* **🖼️ Full CG Gallery**: Unlocks all illustrations and animations in the Extras Gallery.
* **🎬 All Scene Replays**: Unlocks all 765 interactive and story replays in the Replay Gallery.
* **👑 Patron & Supporter Tier 3**: Activates subscriber-exclusive paths, variants, and animations.
* **👗 Outfits & Key Items**: Unlocks all shop outfits and key items directly in the player inventory.

### 📊 2. Character & Relationship Stats
* Directly adjust and monitor character progression with real-time level synchronization:
  * **Hinata**: Love, Obedience, Corruption (plus legacy tolerance tiers)
  * **Himawari**: Love, Obedience
  * **MC (Boruto)**: Dominance, Hatred
* Fast modifier buttons: **`-10`**, **`-1`**, **`+1`**, **`+10`**, and **`MAX (100)`**.
* **⚡ Max All Stats**: Maximizes all character stats to 100 simultaneously.

### ⚡ 3. MC Physical & Skills
* **Physical Strength** (`strengthlevel`): Adjust from 0 to 100.
* **Massage Knowledge** (`massageknowledge`): Adjust from 1 to 10.
* **⚡ Max Both Skills**: One-click skill maximization.

### 💰 4. Economy & Inventory
* **Player Cash**: Increment **`+¥1,000`**, **`+¥10,000`**, **`+¥50,000`**, or **`SET ¥999,999`**.
* **Ramen Currency**: Increment **`+¥500`**, **`+¥2,000`**, **`+¥10,000`**, or **`SET ¥50,000`**.
* **Full Inventory Outfits & Items**: View bag quantities and add individual items or batch add all 12:
  * *Camera*, *Bikini*, *Black Dress*, *Massage Tips Vol. 1*, *Blindfold*, *Home Pool*, *Swimsuit*, *Cammy Cosplay*, *Chun-Li Cosplay*, *Maid Outfit*, *Slave Outfit*, *Lockpicks*.

### ⏳ 5. Calendar & Time Control
* **Time of Day**: Jump to **🌅 Morning (0)**, **🌆 Evening (1)**, or **🌙 Night (2)**, or step forward with **`⏩ Advance +1 Period`**.
* **Calendar Days**: Fast advance **`+1 Day`**, **`+5 Days`**, rewind **`⏪ -1 Day`**, or jump directly to **Day 1, 5, 10, 15, 20, 25, 30**.

### 📜 6. Quests & Journal
* **🔓 Unlock All Pending Quests**: Unlocks pending journal objectives across Boruto, Hinata, and Himawari quest logs.
* **✅ Complete All Quests**: Marks active quests as completed.

---

## 🎮 How to Use in Game

| Method | Action |
| :--- | :--- |
| **Floating Badge** | Click the **`[⚡ MOD]`** badge in the top-right corner of the screen |
| **Hotkey 1** | Press **`F8`** anytime during dialogue, free roam, or menus |
| **Hotkey 2** | Press **`~`** (backtick / tilde key) |
| **Close Menu** | Press **`Esc`**, **`F8`**, **`~`**, or click **`✕ CLOSE`** |

---

## 📦 Installation

### Method A: Automated Installer (Windows)
1. Download or clone this repository.
2. Run `install.bat`.
3. If not placed directly in the game folder, it will prompt you to enter your House of Shinobi game path.
4. Launch the game!

### Method B: Manual Drag & Drop
1. Copy the `game/` folder from this repository.
2. Paste it into your main House of Shinobi installation folder (where `HoS.exe` or `HoS.py` is located).
3. Confirm replacing files if prompted.
4. *(Optional but recommended)*: Delete any `*.rpyb` files in `game/cache/` to ensure fresh cache generation.
5. Launch the game!

---

## 🛡️ Anti-Tamper & Technical Architecture

House of Shinobi includes a custom Cython-compiled integrity checker (`_glcache.pyd`) that performs checksums on Ren'Py engine files (`renpy/*.py`) and rejects loose `.rpy` scripts placed in `game/`.

This mod bypasses these checks cleanly by:
1. Bootstrapping via `game/python-packages/guide_logic.py`, which is imported by Ren'Py without DRM hash checks.
2. Compiling the complete UI and screen hierarchy directly into Ren'Py's in-memory AST via `renpy.game.script.load_string(...)` without generating unmonitored scripts on disk.
3. Automatically syncing with the game's internal `Stat` objects and rollback log for 100% save safety.

---

## ⚖️ License
Released under the [MIT License](LICENSE).
