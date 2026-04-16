#!/usr/bin/env python3
"""Trigger bilingual (zh + en) artifact generation for all notebooks.

Cultural content (易经/道德经/黄帝内经/孙子兵法): primary zh, also en for international
Euclid / Papers: primary en, also zh for Chinese audience

Outputs are downloaded with language suffix:
    {slug}_video_zh.mp4 / {slug}_video_en.mp4
    {slug}_infographic_zh.png / {slug}_infographic_en.png
    {slug}_slides_zh.pdf / {slug}_slides_en.pdf

Usage:
    python tools/bilingual_generation.py --trigger       # Trigger missing
    python tools/bilingual_generation.py --download      # Download completed
    python tools/bilingual_generation.py --status        # Show status
"""

import argparse
import asyncio
from pathlib import Path

from notebooklm import NotebookLMClient

ARTIFACTS = Path(__file__).parent.parent / "workspace" / "artifacts"

# Which notebooks are primarily Chinese vs English
def is_chinese_primary(title: str) -> bool:
    """Cultural content is zh primary; papers/euclid are en primary."""
    zh_markers = [
        "cosmic_timing", "organ_governance", "channels_networks", "diagnosis_pulse",
        "pathogenesis", "needling_law", "qi_blood", "spirit_emotion", "excess_deficiency",
        "longevity", "pain_bi_jue", "integrative_doctrine",  # 黄帝内经
        "generative_ground", "binary_duality", "wu_wei", "emptiness_receptivity",
        "de_nourishment", "return_reversal", "governance_statecraft", "softness_yielding",
        "sufficiency_limits", "hierarchy_resolution", "naturalness_simplicity", "mysterious_unity",  # 道德经
        "primal_creation", "dynamic_change", "obstruction_danger", "stillness_restraint",
        "strength_power", "receptivity_nourishment", "mutual_influence", "revolution_transformation",
        "gradual_progress", "illumination_discernment", "limitation_moderation", "gathering_dispersal",  # 易经
        "strategic_estimation", "speed_logistics", "total_victory", "dispositions_defense",
        "configuration_energy", "weakness_strength", "maneuver_variation", "marching_field",
        "terrain_topology", "fire_attack",  # 孙子兵法
        "hexagram",
    ]
    title_l = title.lower()
    return any(m in title_l for m in zh_markers)


def slug_for(nb_title: str) -> str:
    return nb_title.replace("Omega: ", "").replace("Omega Master: ", "master_").replace(" ", "_").replace("/", "_")[:100]


async def trigger_all(client, language: str):
    """Trigger video/infographic/slides in given language for all notebooks."""
    nbs = await client.notebooks.list()
    omega_nbs = [nb for nb in nbs if "Omega" in nb.title or any(k in nb.title for k in ["Jtp","Grg","Etds","Siads","Rairo","Jnt","Rint","Fibonacci","Zeckendorf","Zero Jitter","Folding","Branch"])]

    triggered = {"video": 0, "infographic": 0, "slides": 0}
    for nb in omega_nbs:
        # For now, trigger Chinese version for Chinese-primary, English for others
        target_lang = "zh" if is_chinese_primary(nb.title) else "en"
        if target_lang != language:
            continue

        for kind, gen_fn in [
            ("video", client.artifacts.generate_video),
            ("infographic", lambda nid: client.artifacts.generate_infographic(nid, language=language)),
            ("slides", lambda nid: client.artifacts.generate_slide_deck(nid, language=language)),
        ]:
            try:
                if kind == "video":
                    await gen_fn(nb.id, language=language)
                else:
                    await gen_fn(nb.id)
                triggered[kind] += 1
                await asyncio.sleep(0.5)
            except Exception as e:
                pass
        print(f"  [triggered {language}] {nb.title[:55]}")

    print(f"\nTriggered {language}: {triggered}")


async def trigger_chinese(args):
    async with await NotebookLMClient.from_storage() as c:
        await trigger_all(c, "zh")


async def trigger_english(args):
    async with await NotebookLMClient.from_storage() as c:
        await trigger_all(c, "en")


async def status(args):
    async with await NotebookLMClient.from_storage() as c:
        nbs = await c.notebooks.list()
        omega_nbs = [nb for nb in nbs if "Omega" in nb.title]
        zh = sum(1 for nb in omega_nbs if is_chinese_primary(nb.title))
        en = len(omega_nbs) - zh
        print(f"Total notebooks: {len(omega_nbs)}")
        print(f"  Chinese-primary: {zh}")
        print(f"  English-primary: {en}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trigger-zh", action="store_true", help="Trigger Chinese generation")
    parser.add_argument("--trigger-en", action="store_true", help="Trigger English generation")
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()

    if args.trigger_zh:
        asyncio.run(trigger_chinese(args))
    elif args.trigger_en:
        asyncio.run(trigger_english(args))
    elif args.status:
        asyncio.run(status(args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
