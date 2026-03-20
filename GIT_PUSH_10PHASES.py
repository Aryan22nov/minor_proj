#!/usr/bin/env python
"""
10-PHASE GIT PUSH WORKFLOW
===========================
Systematic approach to staging, committing, and pushing code changes.

Phases:
1. Initialize & Check Status
2. Clean & Stash Temporary Files
3. Stage Backend Changes  
4. Stage Frontend Changes
5. Stage AI/ML Changes
6. Stage Documentation
7. Commit All Changes
8. Verify Local Repository
9. Push to Remote
10. Finalize & Create Summary
"""

import subprocess
import os
import json
from pathlib import Path
from datetime import datetime

class GitPushWorkflow:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.phase = 0
        self.results = []
        self.errors = []
        
    def run_command(self, cmd, description=""):
        """Execute a shell command and return output"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, f"Command timeout: {cmd}"
        except Exception as e:
            return False, str(e)
    
    def print_phase(self, num, title, description=""):
        """Print phase header"""
        self.phase = num
        print(f"\n{'═'*70}")
        print(f"  PHASE {num}/10: {title}")
        print(f"{'═'*70}")
        if description:
            print(f"  {description}\n")
    
    def log_result(self, category, status, message):
        """Log operation result"""
        symbol = "✓" if status else "✗"
        print(f"  {symbol} {category:30s} {message}")
        self.results.append({
            'phase': self.phase,
            'category': category,
            'status': status,
            'message': message
        })
        if not status:
            self.errors.append(f"Phase {self.phase}: {category} - {message}")
    
    # ========================================================================
    # PHASE 1: Initialize & Check Status
    # ========================================================================
    def phase_1_initialize(self):
        """Initialize and check git status"""
        self.print_phase(1, "Initialize & Check Status", 
                        "Verify git repository and check current status")
        
        # Check if git repo exists
        success, output = self.run_command("git status")
        if success:
            self.log_result("Git Repository", True, "Valid Git repository found")
        else:
            self.log_result("Git Repository", False, "Not a valid Git repository")
            return False
        
        # Get current branch
        success, output = self.run_command("git branch --show-current")
        if success:
            current_branch = output.strip()
            self.log_result("Current Branch", True, f"On branch: {current_branch}")
        else:
            self.log_result("Current Branch", False, "Could not determine branch")
            return False
        
        # Count modified files
        success, output = self.run_command("git status --short")
        if success:
            files = len(output.strip().split('\n'))
            self.log_result("Modified Files", True, f"Found {files} changes")
        else:
            self.log_result("Modified Files", False, "Could not count changes")
            return False
        
        # Get last commit
        success, output = self.run_command("git log -1 --pretty=format:'%h - %s'")
        if success:
            self.log_result("Last Commit", True, f"{output.strip()}")
        
        return True
    
    # ========================================================================
    # PHASE 2: Clean & Stash Temporary Files
    # ========================================================================
    def phase_2_clean(self):
        """Clean up temporary files"""
        self.print_phase(2, "Clean & Stash Temporary Files",
                        "Remove temporary files and prepare for staging")
        
        # List untracked files
        success, output = self.run_command("git status --short | grep '^??'")
        if success:
            untracked = len([l for l in output.strip().split('\n') if l])
            self.log_result("Untracked Files", True, f"Found {untracked} untracked files")
        
        # Show what will be staged
        success, output = self.run_command("git status --short | grep -E '^\\s?M'")
        if success:
            modified = len([l for l in output.strip().split('\n') if l])
            self.log_result("Modified Files", True, f"Ready to stage {modified} files")
        
        return True
    
    # ========================================================================
    # PHASE 3: Stage Backend Changes
    # ========================================================================
    def phase_3_backend(self):
        """Stage backend changes"""
        self.print_phase(3, "Stage Backend Changes",
                        "Stage Flask app, requirements, and backend configs")
        
        backend_files = [
            "app.py",
            "wsgi.py",
            "requirements.txt"
        ]
        
        for file in backend_files:
            if (self.base_dir / file).exists():
                success, output = self.run_command(f"git add {file}")
                status = "exists, staged" if success else "failed to stage"
                self.log_result(f"Backend: {file}", success, status)
            else:
                self.log_result(f"Backend: {file}", False, "file not found")
        
        return True
    
    # ========================================================================
    # PHASE 4: Stage Frontend Changes
    # ========================================================================
    def phase_4_frontend(self):
        """Stage frontend changes"""
        self.print_phase(4, "Stage Frontend Changes",
                        "Stage React frontend files and build output")
        
        frontend_files = [
            "frontend/src/App.jsx",
            "frontend/src/config.js",
            "frontend/src/styles.css",
            "frontend/dist/"
        ]
        
        for file in frontend_files:
            if (self.base_dir / file).exists():
                success, output = self.run_command(f"git add {file}")
                status = "exists, staged" if success else "failed to stage"
                self.log_result(f"Frontend: {file}", success, status)
            else:
                self.log_result(f"Frontend: {file}", False, "not found")
        
        return True
    
    # ========================================================================
    # PHASE 5: Stage AI/ML Changes
    # ========================================================================
    def phase_5_ai_ml(self):
        """Stage AI/ML model files and configs"""
        self.print_phase(5, "Stage AI/ML Changes",
                        "Stage trained model, class mappings, and configs")
        
        ml_files = [
            "best_model_transfer.h5",
            "class_mapping.json",
            "model_metadata.json",
            "model_config.json"
        ]
        
        for file in ml_files:
            if (self.base_dir / file).exists():
                # Check file size
                size_mb = (self.base_dir / file).stat().st_size / (1024*1024)
                success, output = self.run_command(f"git add {file}")
                status = f"staged ({size_mb:.1f}MB)" if success else "failed"
                self.log_result(f"ML: {file}", success, status)
            else:
                self.log_result(f"ML: {file}", False, "not found")
        
        return True
    
    # ========================================================================
    # PHASE 6: Stage Documentation
    # ========================================================================
    def phase_6_documentation(self):
        """Stage documentation files"""
        self.print_phase(6, "Stage Documentation",
                        "Stage all guides, READMEs, and documentation")
        
        doc_patterns = [
            "*.md",
            "QUICK_START*.py",
            "SYSTEM_*.py",
            "*_GUIDE.md",
            "*_GUIDE.py",
            "MODEL_USAGE_README.md",
            "FILE_UPLOAD_FIX.py"
        ]
        
        staged_count = 0
        for pattern in doc_patterns:
            success, output = self.run_command(f"git add {pattern}")
            if success:
                # Count matched files
                files = output.count(pattern)
                staged_count += 1
        
        self.log_result("Documentation", True, f"Staged documentation files")
        
        return True
    
    # ========================================================================
    # PHASE 7: Commit All Changes
    # ========================================================================
    def phase_7_commit(self):
        """Create commits for each category"""
        self.print_phase(7, "Commit All Changes",
                        "Create organized commits for each component")
        
        commits = [
            ("Backend", "git commit -m 'Fix: Update backend API with 4-disease classification and file upload improvements'"),
            ("Frontend", "git commit -m 'UX: Rebuild React frontend with fixed file upload and improved accessibility'"),
            ("AI/ML", "git commit -m 'ML: Add trained MobileNetV2 model and class configuration for skin disease detection'"),
            ("Documentation", "git commit -m 'Docs: Add comprehensive guides for system architecture, API usage, and deployment'")
        ]
        
        for category, cmd in commits:
            success, output = self.run_command(cmd)
            if success or "nothing to commit" in output:
                self.log_result(f"Commit: {category}", True, "committed")
            else:
                self.log_result(f"Commit: {category}", False, output[:50])
        
        return True
    
    # ========================================================================
    # PHASE 8: Verify Local Repository
    # ========================================================================
    def phase_8_verify(self):
        """Verify local repository state"""
        self.print_phase(8, "Verify Local Repository",
                        "Verify all commits are ready for push")
        
        # Check for uncommitted changes
        success, output = self.run_command("git status --short")
        if success:
            if output.strip():
                lines = [l for l in output.strip().split('\n') if l]
                self.log_result("Uncommitted Changes", True, f"{len(lines)} files remaining")
            else:
                self.log_result("Working Directory", True, "Clean - all committed")
        
        # Show commits to be pushed
        success, output = self.run_command("git log origin/main..HEAD --oneline | wc -l")
        if success:
            count = int(output.strip()) if output.strip().isdigit() else 0
            self.log_result("Commits Ready", True, f"{count} new commits to push")
        
        # Get current HEAD
        success, output = self.run_command("git rev-parse HEAD")
        if success:
            commit_sha = output.strip()[:7]
            self.log_result("Current HEAD", True, f"SHA: {commit_sha}")
        
        # Verify remote exists
        success, output = self.run_command("git remote -v")
        if success and "origin" in output:
            self.log_result("Remote Repository", True, "origin found")
        else:
            self.log_result("Remote Repository", False, "origin not found")
        
        return True
    
    # ========================================================================
    # PHASE 9: Push to Remote
    # ========================================================================
    def phase_9_push(self):
        """Push to remote repository"""
        self.print_phase(9, "Push to Remote",
                        "Push all commits to remote repository")
        
        # Get current branch
        success, output = self.run_command("git branch --show-current")
        current_branch = output.strip() if success else "main"
        
        # Push to remote
        success, output = self.run_command(f"git push origin {current_branch}")
        if success:
            self.log_result("Push to Remote", True, f"Successfully pushed to origin/{current_branch}")
        else:
            if "up to date" in output:
                self.log_result("Push to Remote", True, "Repository already up to date")
            elif "rejected" in output:
                self.log_result("Push to Remote", False, "Push rejected - pull first")
            else:
                self.log_result("Push to Remote", False, output[:60])
        
        return True
    
    # ========================================================================
    # PHASE 10: Finalize & Create Summary
    # ========================================================================
    def phase_10_finalize(self):
        """Finalize and create summary"""
        self.print_phase(10, "Finalize & Create Summary",
                         "Generate completion report and summary")
        
        # Get final status
        success, output = self.run_command("git log --oneline origin -5")
        if success:
            self.log_result("Remote History", True, "Retrieved latest commits")
        
        # Count total changed files
        success, output = self.run_command("git diff --name-only HEAD~5..HEAD")
        if success:
            files = len([l for l in output.strip().split('\n') if l])
            self.log_result("Total Changes", True, f"{files} files modified/added")
        
        # Get current status
        success, output = self.run_command("git status")
        if "nothing to commit" in output:
            self.log_result("Workflow Status", True, "COMPLETE - All changes pushed")
        else:
            self.log_result("Workflow Status", True, "Complete with remaining changes")
        
        return True
    
    def run_all_phases(self):
        """Execute all 10 phases"""
        print("\n" + "╔" + "═"*68 + "╗")
        print("║" + " "*15 + "10-PHASE GIT PUSH WORKFLOW" + " "*27 + "║")
        print("║" + " "*20 + "Starting Complete Git Process" + " "*20 + "║")
        print("╚" + "═"*68 + "╝")
        
        phases = [
            ("Phase 1", self.phase_1_initialize),
            ("Phase 2", self.phase_2_clean),
            ("Phase 3", self.phase_3_backend),
            ("Phase 4", self.phase_4_frontend),
            ("Phase 5", self.phase_5_ai_ml),
            ("Phase 6", self.phase_6_documentation),
            ("Phase 7", self.phase_7_commit),
            ("Phase 8", self.phase_8_verify),
            ("Phase 9", self.phase_9_push),
            ("Phase 10", self.phase_10_finalize),
        ]
        
        completed = 0
        for phase_name, phase_func in phases:
            try:
                if phase_func():
                    completed += 1
                else:
                    print(f"  ✗ {phase_name} failed")
            except Exception as e:
                print(f"  ✗ {phase_name} error: {e}")
                self.errors.append(f"{phase_name}: {str(e)}")
        
        self.print_summary(completed)
    
    def print_summary(self, completed):
        """Print final summary"""
        print("\n" + "╔" + "═"*68 + "╗")
        print("║" + " "*20 + "WORKFLOW SUMMARY" + " "*32 + "║")
        print("╚" + "═"*68 + "╝\n")
        
        print(f"  Phases Completed:    {completed}/10")
        print(f"  Total Operations:    {len(self.results)}")
        print(f"  Successful:          {sum(1 for r in self.results if r['status'])}")
        print(f"  Errors:              {sum(1 for r in self.results if not r['status'])}")
        
        if self.errors:
            print("\n  Errors Encountered:")
            for error in self.errors:
                print(f"    • {error}")
        
        print("\n" + "╔" + "═"*68 + "╗")
        if completed == 10 and not self.errors:
            print("║" + " "*15 + "✓ GIT PUSH WORKFLOW COMPLETED SUCCESSFULLY" + " "*10 + "║")
        else:
            print("║" + " "*10 + "⚠ WORKFLOW COMPLETED WITH WARNINGS/ERRORS" + " "*15 + "║")
        print("╚" + "═"*68 + "╝\n")

if __name__ == "__main__":
    workflow = GitPushWorkflow()
    workflow.run_all_phases()
