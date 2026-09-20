import "@supabase/functions-js/edge-runtime.d.ts";
import { withSupabase } from "@supabase/server";

export default {
  fetch: withSupabase({ auth: "none" }, async (request, ctx) => {
    if (request.method !== "GET") {
      return Response.json(
        { error: "Method not allowed" },
        { status: 405, headers: { Allow: "GET" } },
      );
    }

    const { data, error } = await ctx.supabaseAdmin
      .from("messages")
      .select("*")
      .order("created_at", { ascending: false });

    if (error) {
      console.error(error);
      return Response.json({ error: "Could not load messages" }, { status: 500 });
    }

    return Response.json(data, {
      headers: { "Cache-Control": "no-store" },
    });
  }),
};
