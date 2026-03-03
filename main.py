import sys
import argparse
from rich.console import Console
from rich.panel import Panel

from modules.dictionary_gen import DictionaryGenerator
from modules.strength_analyzer import PasswordStrengthAnalyzer
from modules.brute_force_sim import BruteForceSimulator
from modules.hash_extractor_sim import HashExtractorSim
from modules.report_generator import ReportGenerator
import json
import time

console = Console()

def display_banner():
    banner_text = """
    [bold cyan]QYLATRIX OFFENSIVE SECURITY SUITE[/bold cyan]
    [blue]Advanced toolkit for password policy testing and security assessment.[/blue]
    """
    console.print(Panel.fit(banner_text, border_style="cyan"))

def interactive_menu():
    dict_gen = DictionaryGenerator()
    analyzer = PasswordStrengthAnalyzer()
    simulator = BruteForceSimulator()
    extractor = HashExtractorSim()
    reporter = ReportGenerator()
    
    while True:
        console.print("\n[bold cyan]--- Qylatrix Main Menu ---[/bold cyan]")
        console.print("1. Dictionary Generator")
        console.print("2. Password Strength Analyzer")
        console.print("3. Brute-Force Simulator")
        console.print("4. Hash Extraction & Parsing")
        console.print("5. Generate Audit Report")
        console.print("6. Exit")
        
        choice = console.input("[bold cyan]Select an option (1-6): [/bold cyan]")
        
        if choice == '1':
            words = console.input("Enter base words separated by comma: ").split(',')
            words = [w.strip() for w in words if w.strip()]
            if not words: continue
            
            base_set = dict_gen.generate_base_words(words)
            mutated = dict_gen.apply_mutations(base_set)
            
            out_file = console.input("Enter output filename [custom_wordlist.txt]: ").strip() or "custom_wordlist.txt"
            count = dict_gen.export_wordlist(mutated, out_file)
            console.print(f"[green]Successfully generated {count} words and saved to {out_file}[/green]")
            
        elif choice == '2':
            pwd = console.input("Enter password to analyze: ")
            if not pwd: continue
            
            res = analyzer.analyze(pwd)
            recs = analyzer.generate_recommendations(res)
            
            console.print("\n[bold]Analysis Results:[/bold]")
            console.print(f"Score: {res['score']}/4")
            console.print(f"Entropy: {res['math_entropy_bits']} bits")
            console.print(f"Estimated Crack Time: {res['crack_times_display'].get('offline_fast_hashing_1e10_per_second', 'Unknown')}")
            if recs:
                console.print("\n[yellow]Recommendations:[/yellow]")
                for r in recs:
                    console.print(f"- {r}")
                    
        elif choice == '3':
            console.print("1. Dictionary Attack\n2. Brute-Force Time Estimation")
            sub = console.input("Choose (1-2): ")
            
            if sub == '1':
                tgt = console.input("Enter target hash (MD5/SHA256): ")
                wl = console.input("Enter wordlist path [custom_wordlist.txt]: ").strip() or "custom_wordlist.txt"
                h_type = console.input("Hash type (md5/sha256) [md5]: ").strip() or "md5"
                
                console.print("[cyan]Running simulation...[/cyan]")
                res = simulator.simulate_dictionary_attack(tgt, wl, h_type)
                if 'error' in res:
                    console.print(f"[red]{res['error']}[/red]")
                else:
                    console.print(f"Found: [green]{res['success']}[/green]")
                    if res['success']:
                        console.print(f"Password: [bold red]{res['password']}[/bold red]")
                    console.print(f"Time Taken: {res['time_taken_seconds']:.2f}s")
                    console.print(f"Hashes/sec: {res['hashes_per_second']:.0f}")
                    
            elif sub == '2':
                pwd = console.input("Enter a sample password length/complexity to simulate: ")
                htype = console.input("Enter assumed hash type (md5/sha512/ntlm/bcrypt) [ntlm]: ").strip() or "ntlm"
                
                res = simulator.estimate_brute_force_time(pwd, hash_type=htype)
                console.print("\n[bold]Brute-Force Estimate:[/bold]")
                console.print(f"Combinations: {res['combinations']:,}")
                console.print(f"Assumed Hash Rate: {res['assumed_hash_rate']:,} H/s")
                console.print(f"Estimated Time: [red]{res['formatted_time']}[/red]")
                
        elif choice == '4':
            console.print("1. Parse Linux Shadow\n2. Parse Windows SAM Dump")
            sub = console.input("Choose (1-2): ")
            
            if sub == '1':
                 file = console.input("Enter shadow file path [test_shadow.txt]: ").strip() or "test_shadow.txt"
                 accounts = extractor.parse_linux_shadow(file)
                 for acc in accounts:
                     console.print(acc)
                     
            elif sub == '2':
                 file = console.input("Enter SAM dump file path [test_sam.txt]: ").strip() or "test_sam.txt"
                 accounts = extractor.parse_windows_sam_dump(file)
                 for acc in accounts:
                     console.print(acc)
                     
        elif choice == '5':
            # Run a simulated audit on a few passwords to generate report
            passwords = ["password123", "admin", "P@ssw0rd2024!", "correct horse battery staple"]
            console.print(f"[cyan]Running sample audit on: {', '.join(passwords)}...[/cyan]")
            
            results = []
            for p in passwords:
                res = analyzer.analyze(p)
                # Attach the actual password for the report logic, but recommendations logic needs feedback from result
                results.append(res)
                
            fname = reporter.generate_audit_report(results)
            console.print(f"[green]Audit report generated: {fname}[/green]")
            
        elif choice == '6':
            console.print("[yellow]Exiting...[/yellow]")
            break
        else:
            console.print("[red]Invalid choice. Try again.[/red]")


def main():
    parser = argparse.ArgumentParser(description="Qylatrix Offensive Security Suite")
    parser.add_argument("--interactive", "-i", action="store_true", help="Launch interactive menu mode")
    args = parser.parse_args()

    display_banner()

    if args.interactive:
        console.print("[yellow]Launching Interactive Mode...[/yellow]")
        interactive_menu()
    else:
        parser.print_help()
        console.print("\n[cyan]Tip: Use --interactive to launch the menu.[/cyan]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting...[/bold red]")
        sys.exit(0)
