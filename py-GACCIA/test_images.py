from gaccia_agents_with_images import EnhancedGACCIAOrchestrator

def test_single_image():
    orchestrator = EnhancedGACCIAOrchestrator()
    
    # Test image generation
    prompt = "Epic coding battle between Python and TypeScript, dramatic and competitive"
    image_path = orchestrator._create_image(prompt, "test_battle")
    
    if image_path:
        print(f"✅ Image generated successfully: {image_path}")
    else:
        print("❌ Image generation failed")

if __name__ == "__main__":
    test_single_image()