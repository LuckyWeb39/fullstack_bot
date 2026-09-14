import "@supabase/functions-js/edge-runtime.d.ts";
import { withSupabase } from "@supabase/server";

export default {
  fetch: withSupabase({ auth: "none" }, async (req) => {
    if (req.method !== "GET") {
      return Response.json(
          { error: "Method not allowed" },
          {
            status: 405,
            headers: { Allow: "GET" },
          },
      );
    }

    return Response.json({
      message: "hello, IT-INCUBATOR",
      studentsID: "5197",
    });
  }),
};