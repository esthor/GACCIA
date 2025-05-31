import { anthropic, Inngest } from "inngest";

const inngest = new Inngest({ id: "anthropic-claude-pdf-processing" });

const pdfFunction = inngest.createFunction(
  { id: "pdf-function" },
  { event: "pdf-function/event" },
  async ({ step }) => {
    const result = await step.ai.infer("parse-pdf", {
      model: anthropic({
        model: "claude-3-5-sonnet-latest",
        defaultParameters: { max_tokens: 3094 },
      }),
      body: {
        messages: [
          {
            role: "user",
            content: [
              {
                type: "document",
                source: {
                  type: "url",
                  url: "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf",
                },
              },
              {
                type: "text",
                text: "What are the key findings in this document?",
              },
            ],
          },
        ],
      },
    });

    const findings = result.content[0].type === "text"
      ? result.content[0].text
      : result.content[0];
      
    
    // ... AgentKit Agents and Network definition ...
    
    researchNetwork.run(`Given the following key findings, find related documents and topics: ${findings}`)
    
  }
);