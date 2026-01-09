import os
import json
import glob
import re
from datetime import datetime, timedelta
from collections import defaultdict
import argparse

class ReadmeUpdater:
    def __init__(self, repo_path="."):
        self.repo_path = repo_path
        self.stats_file = os.path.join(repo_path + '/data/', "stats.json")
        self.readme_file = os.path.join(repo_path, "README.md")
        self.stats = self.load_stats()

    # ---------- LOAD / SAVE ----------
    def load_stats(self):    
        default = {
            "total_problems": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "days_active": 0,
            "platform_stats": {
                "leetcode": 0,
                "codeforces": 0,
                "geeksforgeeks": 0
                
            },
            "category_stats": {},
            "language_stats": {},
            "difficulty_stats": {
                "Easy": 0,
                "Medium": 0,
                "Hard": 0
            },
            "last_updated": ""
        }

        if not os.path.exists(self.stats_file):
            return default

        with open(self.stats_file, "r") as f:
            data = json.load(f)

        # 🔒 Ensure backward compatibility
        for key, value in default.items():
            if key not in data:
                data[key] = value

        # Ensure nested keys
        for p in default["platform_stats"]:
            data["platform_stats"].setdefault(p, 0)

        for d in default["difficulty_stats"]:
            data["difficulty_stats"].setdefault(d, 0)

        return data
        

    def save_stats(self):
        self.stats["category_stats"] = dict(self.stats["category_stats"])
        self.stats["language_stats"] = dict(self.stats["language_stats"])
        with open(self.stats_file, "w") as f:
            json.dump(self.stats, f, indent=2)

    # ---------- COUNT SOLUTIONS ----------
    def count_solutions(self):
        self.stats["category_stats"] = defaultdict(int)
        self.stats["language_stats"] = defaultdict(int)
        self.stats["difficulty_stats"] = {"Easy": 0, "Medium": 0, "Hard": 0}

        extensions = {
            ".py": "Python",
            ".cpp": "C++",
            ".js": "JavaScript",
            ".c": "C",
            ".rs": "Rust",
        }

        total = 0
        platforms = ["leetcode", "codeforces", "geeksforgeeks"]

        for platform in platforms:
            base = os.path.join(self.repo_path, "platforms", platform)
            count = 0

            for ext, lang in extensions.items():
                files = glob.glob(f"{base}/**/*{ext}", recursive=True)
                count += len(files)
                total += len(files)

                for f in files:
                    self.stats["language_stats"][lang] += 1
                    p = f.lower()
                    if "/easy/" in p:
                        self.stats["difficulty_stats"]["Easy"] += 1
                    elif "/medium/" in p:
                        self.stats["difficulty_stats"]["Medium"] += 1
                    elif "/hard/" in p:
                        self.stats["difficulty_stats"]["Hard"] += 1

            self.stats["platform_stats"][platform] = count

        problems_path = os.path.join(self.repo_path, "problems")
        if os.path.exists(problems_path):
            for topic in os.listdir(problems_path):
                topic_path = os.path.join(problems_path, topic)
                if os.path.isdir(topic_path):
                    for ext in extensions:
                        self.stats["category_stats"][topic.replace("-", " ").title()] += \
                            len(glob.glob(f"{topic_path}/**/*{ext}", recursive=True))

        self.stats["total_problems"] = total

    # ---------- STREAK ----------
    def update_streak(self):
        streak_file = os.path.join(self.repo_path + '/data/', "streaks.json")
        data = {"dates": []}

        if os.path.exists(streak_file):
            with open(streak_file, "r") as f:
                data = json.load(f)

        today = datetime.now().date()
        if today.isoformat() not in data["dates"]:
            data["dates"].append(today.isoformat())

        dates = sorted(datetime.strptime(d, "%Y-%m-%d").date() for d in data["dates"])

        longest = current = temp = 1
        for i in range(1, len(dates)):
            if (dates[i] - dates[i - 1]).days == 1:
                temp += 1
            else:
                longest = max(longest, temp)
                temp = 1
        longest = max(longest, temp)

        if dates[-1] == today or dates[-1] == today - timedelta(days=1):
            current = temp
        else:
            current = 0

        with open(streak_file, "w") as f:
            json.dump({"dates": [d.isoformat() for d in dates]}, f, indent=2)

        self.stats["current_streak"] = current
        self.stats["longest_streak"] = longest
        self.stats["days_active"] = len(dates)

    # ---------- AI INSIGHT ----------
    def generate_ai_insight(self):
        if not self.stats["category_stats"]:
            return "Start solving problems daily to unlock insights."

        top_category = max(self.stats["category_stats"], key=self.stats["category_stats"].get)
        hard = self.stats["difficulty_stats"]["Hard"]

        if hard == 0:
            return f"You're strong in {top_category}. Start attempting Hard problems."
        elif hard < 5:
            return "Good momentum. Increase Hard problems to grow faster."
        return "Excellent discipline. Focus on advanced Graphs and DP next."

    # ---------- README MARKDOWN ----------
    def generate_stats_markdown(self):
        cat_total = sum(self.stats["category_stats"].values()) or 1
        lang_total = sum(self.stats["language_stats"].values()) or 1

        cat_bars = ""
        for k, v in sorted(self.stats["category_stats"].items(), key=lambda x: x[1], reverse=True):
            pct = int((v / cat_total) * 100)
            bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
            cat_bars += f"{k:<25} {bar} {pct}%\n"

        insight = self.generate_ai_insight()
        d = self.stats["difficulty_stats"]

        return f"""
<!-- AUTO-GENERATED STATS START -->
<div align="center">

### 📊 Progress Overview

| Metric | Value |
|------|------|
| 🎯 Total Problems | {self.stats["total_problems"]} |
| 🔥 Current Streak | {self.stats["current_streak"]} days |
| 🏆 Longest Streak | {self.stats["longest_streak"]} days |
| 📅 Days Active | {self.stats["days_active"]} |

### 🎯 Difficulty Breakdown
| Difficulty | Solved |
|-----------|--------|
| 🟢 Easy | {d["Easy"]} |
| 🟡 Medium | {d["Medium"]} |
| 🔴 Hard | {d["Hard"]} |

### 🧠 AI Daily Insight
> 💡 {insight}

### 📚 Category Distribution
```text
{cat_bars}
```

</div>
<!-- AUTO-GENERATED STATS END -->


"""

    # ---------- UPDATE README ----------
    def update_readme(self):
        with open(self.readme_file, "r", encoding="utf-8") as f:
            content = f.read()

        content = re.sub(
            r"<!-- AUTO-GENERATED STATS START -->.*?<!-- AUTO-GENERATED STATS END -->",
            self.generate_stats_markdown(),
            content,
            flags=re.DOTALL
        )

        today = datetime.now().strftime("%Y-%m-%d")
        content = re.sub(r"Last Updated: `.*?`", f"Last Updated: `{today}`", content)

        with open(self.readme_file, "w", encoding="utf-8") as f:
            f.write(content)

    def run(self):
        self.count_solutions()
        self.update_streak()
        self.stats["last_updated"] = datetime.now().isoformat()
        self.save_stats()
        self.update_readme()
        print("✅ README updated successfully")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", action="store_true")
    args = parser.parse_args()
    updater = ReadmeUpdater()
    if args.template:
        updater.save_stats()
        print("✅ Template initialized")
    else:
        updater.run()
    
