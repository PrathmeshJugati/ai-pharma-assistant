"use client";

import { Pill, RotateCcw } from "lucide-react";

interface Props {
    onNewChat: () => void;
}

export default function Header({ onNewChat }: Props) {
    return (
        <header className="flex-shrink-0 flex items-center justify-between px-6 py-4 bg-white/80 backdrop-blur-md border-b border-slate-100 shadow-sm">
            {/* Logo + Title */}
            <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-teal-500 to-cyan-600 flex items-center justify-center shadow-md">
                    <Pill size={18} className="text-white" />
                </div>
                <div>
                    <h1 className="text-base font-semibold text-slate-800 leading-none">
                        AI Pharma Assistant
                    </h1>
                    <p className="text-xs text-slate-400 mt-0.5">
                        Drug intelligence, powered by AI
                    </p>
                </div>
            </div>

            {/* New Chat Button */}
            <button
                onClick={onNewChat}
                className="flex items-center gap-2 text-xs font-medium text-slate-500 hover:text-teal-600 border border-slate-200 hover:border-teal-300 rounded-xl px-3 py-2 bg-white hover:bg-teal-50 transition-all duration-200"
            >
                <RotateCcw size={13} />
                New Chat
            </button>
        </header>
    );
}
