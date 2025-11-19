"""
Terminal Chatbot Interface
"""
import os
import sys
from typing import Dict
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table
import logging

from rag_system import RAGSystem

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ChatBot:
    def __init__(self):
        self.console = Console()
        self.rag_system = RAGSystem()
        self.running = True
        self.conversation_history = []
        
    def display_welcome(self):
        """Display welcome message"""
        welcome_text = Text("PDF Intelligent Q&A System", style="bold blue")
        subtitle = Text("Academic Document Q&A Assistant based on RAG Technology", style="italic")
        
        self.console.print(Panel.fit(
            f"{welcome_text}\n{subtitle}",
            border_style="blue"
        ))
        
        # Display system information
        info = self.rag_system.get_system_info()
        self.console.print(f"\nSystem Status:")
        self.console.print(f"  • Vector Database: {info['vector_db']['document_count']} documents")
        self.console.print(f"  • LLM Configuration: {'OK' if info['llm_configured'] else 'Not Configured'}")
        
    def display_help(self):
        """Display help information"""
        help_table = Table(title="Available Commands")
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description", style="white")
        
        help_table.add_row("/help", "Show help information")
        help_table.add_row("/info", "Show system information")
        help_table.add_row("/rebuild", "Rebuild knowledge base")
        help_table.add_row("/clear", "Clear conversation history")
        help_table.add_row("/quit", "Exit program")
        help_table.add_row("Direct question", "Input question to start conversation")
        
        self.console.print(help_table)
    
    def display_system_info(self):
        """Display system information"""
        info = self.rag_system.get_system_info()
        
        info_table = Table(title="System Information")
        info_table.add_column("Item", style="cyan")
        info_table.add_column("Value", style="white")
        
        info_table.add_row("Vector Database", f"{info['vector_db']['collection_name']}")
        info_table.add_row("Document Count", str(info['vector_db']['document_count']))
        info_table.add_row("Embedding Model", info['vector_db']['embedding_model'])
        info_table.add_row("LLM Configuration", "OK" if info['llm_configured'] else "Not Configured")
        info_table.add_row("Chunk Size", str(info['config']['chunk_size']))
        info_table.add_row("Retrieval Count", str(info['config']['top_k_results']))
        info_table.add_row("Similarity Threshold", str(info['config']['similarity_threshold']))
        
        self.console.print(info_table)
    
    def display_response(self, response: Dict):
        """Display response"""
        if not response['success']:
            self.console.print(f"[red]Error: {response['answer']}[/red]")
            return
        
        # Display answer
        answer_panel = Panel(
            response['answer'],
            title="Answer",
            border_style="green"
        )
        self.console.print(answer_panel)
        
        # Display sources
        if response['sources']:
            sources_table = Table(title="Reference Sources")
            sources_table.add_column("Document", style="cyan")
            sources_table.add_column("Segment", style="white")
            sources_table.add_column("Similarity", style="yellow")
            sources_table.add_column("Content Preview", style="dim")
            
            for source in response['sources']:
                sources_table.add_row(
                    source['filename'],
                    str(source['chunk_index'] + 1),
                    f"{source['similarity']:.3f}",
                    source['content_preview']
                )
            
            self.console.print(sources_table)
        else:
            self.console.print("[yellow]No relevant sources found[/yellow]")
    
    def handle_command(self, command: str):
        """Handle commands"""
        if command == "/help":
            self.display_help()
        elif command == "/info":
            self.display_system_info()
        elif command == "/rebuild":
            self.console.print("[yellow]Rebuilding knowledge base...[/yellow]")
            self.rag_system.build_knowledge_base(force_rebuild=True)
            self.console.print("[green]Knowledge base rebuild completed![/green]")
        elif command == "/clear":
            self.conversation_history = []
            self.console.print("[green]Conversation history cleared![/green]")
        elif command == "/quit":
            self.console.print("[blue]Goodbye![/blue]")
            self.running = False
        else:
            self.console.print(f"[red]Unknown command: {command}[/red]")
            self.console.print("Type /help to see available commands")
    
    def run(self):
        """Run chatbot"""
        try:
            # Initialize system
            self.console.print("[yellow]Initializing system...[/yellow]")
            self.rag_system.build_knowledge_base()
            
            # Display welcome message
            self.display_welcome()
            self.console.print("\nType /help to see available commands, or ask a question directly")
            
            # Main loop
            while self.running:
                try:
                    user_input = Prompt.ask("\n[bold blue]You[/bold blue]")
                    
                    if not user_input.strip():
                        continue
                    
                    # Handle commands
                    if user_input.startswith("/"):
                        self.handle_command(user_input)
                    else:
                        self.console.print("[yellow]Thinking...[/yellow]")
                        response = self.rag_system.ask_question(user_input, self.conversation_history)
                        self.display_response(response)
                        
                        self.conversation_history.append({"role": "user", "content": user_input})
                        self.conversation_history.append({"role": "assistant", "content": response['answer']})
                        
                        if len(self.conversation_history) > 6:
                            self.conversation_history = self.conversation_history[-6:]
                        
                except KeyboardInterrupt:
                    self.console.print("\n[yellow]Interrupt signal detected[/yellow]")
                    break
                except Exception as e:
                    logger.error(f"Error processing user input: {e}")
                    self.console.print(f"[red]Processing error: {e}[/red]")
            
        except Exception as e:
            logger.error(f"System initialization failed: {e}")
            self.console.print(f"[red]System initialization failed: {e}[/red]")
            sys.exit(1)

def main():
    """Main function"""
    chatbot = ChatBot()
    chatbot.run()

if __name__ == "__main__":
    main()

