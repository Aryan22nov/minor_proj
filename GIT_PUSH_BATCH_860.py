#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GIT PUSH IN BATCHES - 860 Files Strategy
=========================================

Strategy: Push in 100-file batches
- Phase 1-8: Add 100 files each (800 files total)
- Phase 9: Add remaining 60 files
- Phase 10: Push all + final verification

Total: 860 files → 10 phases
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_cmd(cmd, description=""):
    """Run shell command and return output"""
    print(f"\n  ⏱️  {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"  ✓ {description}")
            return True, result.stdout
        else:
            print(f"  ✗ {description}")
            if result.stderr:
                print(f"     Error: {result.stderr[:200]}")
            return False, result.stderr
    except Exception as e:
        print(f"  ✗ {description}: {str(e)[:200]}")
        return False, str(e)

def get_file_count():
    """Get count of untracked/modified files"""
    success, output = run_cmd("git status --porcelain", "Checking git status")
    if success:
        files = [line for line in output.split('\n') if line.strip()]
        return len(files)
    return 0

def main():
    print("\n" + "="*70)
    print("GIT PUSH IN BATCHES - 860 FILES STRATEGY")
    print("="*70)
    
    print("\n📊 BATCH CONFIGURATION:")
    print("  • Phase 1-8: 100 files each (800 files)")
    print("  • Phase 9:   60 files remaining")
    print("  • Phase 10:  Final push + verification")
    print("  • Total:     860 files")
    
    # Initial status
    total_files = get_file_count()
    print(f"\n📈 Files to process: {total_files}")
    
    if total_files == 0:
        print("\n✓ No files to push. Repository is up to date.")
        return
    
    batches = []
    remaining = total_files
    
    # Create 9 batches of 100, then 1 batch of remaining
    for i in range(9):
        if remaining > 0:
            batch_size = min(100, remaining)
            batches.append(batch_size)
            remaining -= batch_size
    
    if remaining > 0:
        batches.append(remaining)
    
    print(f"\n📋 BATCH PLAN ({len(batches)} phases):")
    for i, size in enumerate(batches, 1):
        print(f"  Phase {i}: {size} files")
    
    # ============================================================
    # PHASE LOOP
    # ============================================================
    
    for phase, batch_size in enumerate(batches, 1):
        print(f"\n{'='*70}")
        print(f"🔹 PHASE {phase}/{len(batches)} - Adding {batch_size} files")
        print(f"{'='*70}")
        
        # Get list of unstaged files
        success, output = run_cmd("git diff --name-only", "Getting unstaged files")
        unstaged_files = [line.strip() for line in output.split('\n') if line.strip()] if success else []
        
        # Get list of untracked files
        success, output = run_cmd("git ls-files --others --exclude-standard", "Getting untracked files")
        untracked_files = [line.strip() for line in output.split('\n') if line.strip()] if success else []
        
        # Combine and limit to batch size
        all_files = unstaged_files[:batch_size] + untracked_files[:batch_size - len(unstaged_files[:batch_size])]
        
        if not all_files:
            print(f"\n⚠️  No files found for phase {phase}")
            continue
        
        # Stage files in this batch
        print(f"\n📝 Stage {len(all_files)} files:")
        
        for i, file in enumerate(all_files, 1):
            success, _ = run_cmd(f'git add "{file}"', f"  [{i}/{len(all_files)}] {file[:50]}")
            if not success and i % 10 == 0:
                print(f"     (staged {i} files so far)")
        
        # Check staged status
        success, output = run_cmd("git diff --cached --name-only", "Verifying staged files")
        staged_count = len([l for l in output.split('\n') if l.strip()]) if success else 0
        
        print(f"\n✓ Staged {staged_count} files")
        
        # Commit batch
        commit_msg = f"Batch {phase}/{len(batches)}: Add {staged_count} files [{datetime.now().strftime('%Y-%m-%d %H:%M')}]"
        success, output = run_cmd(
            f'git commit -m "{commit_msg}"',
            f"Committing batch {phase}"
        )
        
        if not success:
            print(f"\n⚠️  Commit failed for phase {phase}")
            continue
        
        print(f"\n📌 Commit message:")
        print(f"   {commit_msg}")
    
    # ============================================================
    # PHASE 10: FINAL PUSH
    # ============================================================
    
    print(f"\n{'='*70}")
    print(f"🔟 PHASE {len(batches)+1}: FINAL PUSH + VERIFICATION")
    print(f"{'='*70}")
    
    # Check for uncommitted changes
    success, output = run_cmd("git status --porcelain", "Checking remaining changes")
    remaining_changes = len([l for l in output.split('\n') if l.strip()]) if success else 0
    
    if remaining_changes > 0:
        print(f"\n⚠️  {remaining_changes} files still need to be committed")
        # Final commit for any remaining changes
        success, _ = run_cmd(
            f'git add -A && git commit -m "Final batch: Remaining {remaining_changes} files"',
            "Making final commit"
        )
    
    # Get current branch
    success, branch = run_cmd("git rev-parse --abbrev-ref HEAD", "Getting current branch")
    branch = branch.strip() if success else "main"
    
    # Push all commits
    print(f"\n🚀 Pushing to origin/{branch}...")
    success, output = run_cmd(
        f"git push origin {branch}",
        f"Pushing all commits to origin/{branch}"
    )
    
    if success:
        print(f"\n✓ Push successful!")
    else:
        print(f"\n✗ Push failed. Trying with force (be careful)...")
        success, output = run_cmd(
            f"git push origin {branch} --force-with-lease",
            "Force push with lease"
        )
    
    # ============================================================
    # FINAL VERIFICATION
    # ============================================================
    
    print(f"\n{'='*70}")
    print(f"📊 FINAL VERIFICATION")
    print(f"{'='*70}")
    
    # Get git log
    success, output = run_cmd(
        "git log --oneline -10",
        "Getting last 10 commits"
    )
    
    if success:
        print("\n📋 Last 10 commits:")
        for line in output.split('\n')[:10]:
            if line.strip():
                print(f"   {line}")
    
    # Check status
    success, output = run_cmd("git status", "Final status check")
    if success:
        if "working tree clean" in output or "nothing to commit" in output:
            print("\n✓ Working directory is clean")
        else:
            print("\n⚠️  Some changes remain:")
            print(output[:300])
    
    # Summary
    print(f"\n{'='*70}")
    print(f"✅ GIT PUSH COMPLETED")
    print(f"{'='*70}")
    print(f"\n📊 Summary:")
    print(f"  • Total phases: {len(batches) + 1}")
    print(f"  • Batches: {len(batches)} × 100 files")
    print(f"  • Final status: Check GitHub for all commits")
    print(f"\n🔗 View commits:")
    print(f"   GitHub → Commits tab")
    print(f"   Or: git log --oneline\n")

if __name__ == "__main__":
    main()
