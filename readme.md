<aside>
<img src="/icons/alien-pixel_purple.svg" alt="/icons/alien-pixel_purple.svg" width="40px" /> **OMG! Create Your BattleBot!**
</aside>

## Game Rules

* **Starting Stats:**
    * 100 Health
    * 80 Ammo
* **Destruction:** 0 Health = Destroyed
* **Per Round:** Each bot attacks one target.
* **Ammo & Damage:** Ammo used = Damage dealt. Attacker loses ammo, target loses health.
* **Destruction Bonus:** Destroying a bot grants +20 Ammo and +20 Health.



## 🔵 Create Your Bot

* **1. Clonne this repo.**
* **2. Setup & Run:** Create a PyCharm project and run the `main` file.
* **3. Duplicate `RandomAttacker`:** Find and duplicate this class at the bottom.
* **4. Rename Your Class:** Give your bot a unique name.
* **5. Implement `attack` Method:**
    * Receives a list of alive `SpaceBots`.
    * Use `BattleBotInterface` methods to get info.
    * **Restriction:** Only use interface methods.
    * **Logic:** Define your attack strategy (who and how much ammo).
    * **Return:** Tuple of (target `SpaceBot`, ammo amount `int`).
    * **Error Handling:** Incorrect returns or exceptions skip your turn!
* **6. Instantiate Your Bot:** In `main`, create an instance of your new bot class.
* **7. Local Game:** Run a game with your bot and `RandomAttacker` bots.
* **8. Refine Strategy:** Adjust your `attack` logic if you lose.

## 🟠 Submit Your Bot

* **1. Local Test:** Ensure your bot works as expected locally and not crashing (!).
* **2. Share Code:** Upload your full code to [codefile.io](https://codefile.io/).
* **3. Send Link:** Privately share the link via Zoom chat.
* **4. Updates:** Use the same link on [codefile.io](https://codefile.io/) to update code.