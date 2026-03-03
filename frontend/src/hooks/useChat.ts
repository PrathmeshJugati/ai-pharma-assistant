"use client";

import { useState, useCallback } from "react";
import { v4 as uuidv4 } from "uuid";
import { Message } from "@/types/chat";
import { sendMessage } from "@/lib/api";

export function useChat() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId] = useState<string>(() => uuidv4());
    const [error, setError] = useState<string | null>(null);

    const addMessage = useCallback((role: Message["role"], content: string) => {
        const msg: Message = {
            id: uuidv4(),
            role,
            content,
            timestamp: new Date(),
        };
        setMessages((prev) => [...prev, msg]);
        return msg;
    }, []);

    const submit = useCallback(
        async (input: string) => {
            const trimmed = input.trim();
            if (!trimmed || isLoading) return;

            setError(null);
            addMessage("user", trimmed);
            setIsLoading(true);

            try {
                const data = await sendMessage(trimmed, sessionId);
                addMessage("assistant", data.response);
            } catch (err) {
                const msg = err instanceof Error ? err.message : "Something went wrong.";
                setError(msg);
                addMessage("assistant", `⚠️ ${msg}`);
            } finally {
                setIsLoading(false);
            }
        },
        [isLoading, sessionId, addMessage]
    );

    const clearChat = useCallback(() => {
        setMessages([]);
        setError(null);
    }, []);

    return { messages, isLoading, error, sessionId, submit, clearChat };
}
