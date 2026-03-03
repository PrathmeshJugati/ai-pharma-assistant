"use client";

import { useEffect, useRef } from "react";
import { AnimatePresence } from "framer-motion";
import { Message } from "@/types/chat";
import MessageBubble from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";

interface Props {
    messages: Message[];
    isLoading: boolean;
}

export default function ChatWindow({ messages, isLoading }: Props) {
    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, isLoading]);

    return (
        <div className="flex-1 overflow-y-auto px-4 py-6 space-y-1 scroll-smooth">
            <AnimatePresence initial={false}>
                {messages.map((msg) => (
                    <MessageBubble key={msg.id} message={msg} />
                ))}
                {isLoading && <TypingIndicator key="typing" />}
            </AnimatePresence>
            <div ref={bottomRef} />
        </div>
    );
}
