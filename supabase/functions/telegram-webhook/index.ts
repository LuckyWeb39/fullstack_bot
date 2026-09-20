import "@supabase/functions-js/edge-runtime.d.ts";
import { withSupabase } from "@supabase/server";

export default {
  fetch: withSupabase({ auth: "none" }, async (request, ctx) => {
    if (request.method !== "POST") {
      return Response.json(
        { error: "Method not allowed" },
        { status: 405, headers: { Allow: "POST" } },
      );
    }

    const expectedSecret = Deno.env.get("TELEGRAM_WEBHOOK_SECRET");
    const receivedSecret = request.headers.get(
      "x-telegram-bot-api-secret-token",
    );

    if (!expectedSecret || receivedSecret !== expectedSecret) {
      return Response.json({ error: "Unauthorized" }, { status: 401 });
    }

    const update = await request.json();
    const message = update.message;

    if (!message?.from || !message.chat) return Response.json({ ok: true });

    const telegramUserId = String(message.from.id);
    const lastMessageAt = new Date(message.date * 1000).toISOString();

    const { data: client, error: clientError } = await ctx.supabaseAdmin
      .from("clients")
      .upsert(
        {
          user_telegram_id: telegramUserId,
          first_name: message.from.first_name ?? null,
          last_name: message.from.last_name ?? null,
          last_message_at: lastMessageAt,
        },
        { onConflict: "user_telegram_id" },
      )
      .select("id")
      .single();

    if (clientError) {
      console.error(clientError);
      return Response.json({ error: "Could not save client" }, { status: 500 });
    }

    const fullName = [message.from.first_name, message.from.last_name]
      .filter(Boolean)
      .join(" ");
    const author = message.from.username || fullName || null;

    const { error: messageError } = await ctx.supabaseAdmin
      .from("messages")
      .insert({
        author,
        body: message.text ?? message.caption ?? null,
        messenger_user_id: telegramUserId,
        messenger_type: "telegram",
        client_id: client.id,
      });

    if (messageError) {
      console.error(messageError);
      return Response.json({ error: "Could not save message" }, { status: 500 });
    }

    const botToken = Deno.env.get("BOT_TOKEN");

    if (!botToken) {
      console.error("BOT_TOKEN is not configured");
      return Response.json({ ok: true });
    }

    const telegramResponse = await fetch(
      `https://api.telegram.org/bot${botToken}/sendMessage`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          chat_id: message.chat.id,
          text: "Все ок, записал!",
        }),
      },
    );

    if (!telegramResponse.ok) {
      console.error("Could not send Telegram confirmation", telegramResponse.status);
    }

    return Response.json({ ok: true });
  }),
};
