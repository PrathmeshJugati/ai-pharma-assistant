"use client";

import { useState, useRef, KeyboardEvent } from "react";
import { SendHorizonal } from "lucide-react";

interface Props {
    onSubmit: (value: string) => void;
    isLoading: boolean;
}

export default function ChatInput({ onSubmit, isLoading }: Props) {
    const [value, setValue] = useState("");
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const handleSubmit = () => {
        if (!value.trim() || isLoading) return;
        onSubmit(value);
        setValue("");
        if (textareaRef.current) {
            textareaRef.current.style.height = "auto";
        }
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setValue(e.target.value);
        // Auto-expand
        const ta = e.target;
        ta.style.height = "auto";
        ta.style.height = `${Math.min(ta.scrollHeight, 160)}px`;
    };

    return (
        <div className="relative flex items-end gap-3 bg-white/70 backdrop-blur-md border border-slate-200 rounded-2xl px-4 py-3 shadow-lg ring-1 ring-slate-100">
            <textarea
                ref={textareaRef}
                value={value}
                onChange={handleChange}
                onKeyDown={handleKeyDown}
                placeholder="Ask about a medicine, substitutes, or prices..."
                rows={1}
                disabled={isLoading}
                className="flex-1 resize-none bg-transparent text-sm text-slate-800 placeholder-slate-400 outline-none leading-relaxed max-h-40 disabled:opacity-50"
            />
            <button
                onClick={handleSubmit}
                disabled={!value.trim() || isLoading}
                className="flex-shrink-0 w-9 h-9 rounded-xl bg-gradient-to-br from-teal-500 to-cyan-600 flex items-center justify-center text-white shadow-md transition-all duration-200 hover:scale-105 hover:shadow-lg active:scale-95 disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
                <SendHorizonal size={16} />
            </button>
        </div>
    );
}
