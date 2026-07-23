"use client";

import { useState, useCallback } from "react";
import { v4 as uuidv4 } from "uuid";
import { Message } from "@/types/chat";
import { sendMessageStream } from "@/lib/api";

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

            const assistantMsgId = uuidv4();
            const initialAssistantMsg: Message = {
                id: assistantMsgId,
                role: "assistant",
                content: "",
                timestamp: new Date(),
            };

            setMessages((prev) => [...prev, initialAssistantMsg]);

            try {
                let fullContent = "";
                for await (const chunk of sendMessageStream(trimmed, sessionId)) {
                    fullContent += chunk;
                    setMessages((prev) =>
                        prev.map((msg) =>
                            msg.id === assistantMsgId
                                ? { ...msg, content: fullContent }
                                : msg
                        )
                    );
                }
            } catch (err) {
                const msg = err instanceof Error ? err.message : "Something went wrong.";
                setError(msg);
                setMessages((prev) =>
                    prev.map((m) =>
                        m.id === assistantMsgId
                            ? { ...m, content: `⚠️ ${msg}` }
                            : m
                    )
                );
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
