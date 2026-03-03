"use client";

import { useCallback } from "react";
import { useChat } from "@/hooks/useChat";
import Header from "@/components/Layout/Header";
import ChatWindow from "@/components/Chat/ChatWindow";
import ChatInput from "@/components/Chat/ChatInput";
import EmptyState from "@/components/Chat/EmptyState";

export default function HomePage() {
  const { messages, isLoading, submit, clearChat } = useChat();

  const handleSuggestion = useCallback(
    (text: string) => {
      submit(text);
    },
    [submit]
  );

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-50 via-cyan-50/30 to-teal-50/40">
      <Header onNewChat={clearChat} />

      <main className="flex flex-col flex-1 overflow-hidden max-w-3xl w-full mx-auto px-0 sm:px-4">
        {messages.length === 0 ? (
          <EmptyState onSuggestion={handleSuggestion} />
        ) : (
          <ChatWindow messages={messages} isLoading={isLoading} />
        )}

        {/* Input bar */}
        <div className="flex-shrink-0 px-4 pb-6 pt-2">
          <ChatInput onSubmit={submit} isLoading={isLoading} />
          <p className="text-center text-[11px] text-slate-400 mt-2">
            AI can make mistakes. Always consult a qualified pharmacist or doctor.
          </p>
        </div>
      </main>
    </div>
  );
}
