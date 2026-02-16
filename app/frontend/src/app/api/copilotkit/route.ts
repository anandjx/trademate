import {
    CopilotRuntime,
    ExperimentalEmptyAdapter,
    copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { HttpAgent } from "@ag-ui/client";
import { NextRequest } from "next/server";

// Create a service adapter for the CopilotKit runtime
const serviceAdapter = new ExperimentalEmptyAdapter();

// Create the main CopilotRuntime instance
const runtime = new CopilotRuntime({
    agents: {
        trademate: new HttpAgent({
            url: "http://localhost:8000/",
        }) as any,
    },
});

// Export the POST handler for the API route
export const POST = async (req: NextRequest) => {
    const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
        runtime,
        serviceAdapter,
        endpoint: "/api/copilotkit",
    });
    return handleRequest(req);
};
