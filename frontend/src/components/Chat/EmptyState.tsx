"use client";

import { motion } from "framer-motion";
import { Search, ArrowLeftRight, MessageCircleQuestion } from "lucide-react";

const suggestions = [
    {
        icon: <Search size={16} />,
        label: "What is Glycomet GP?",
        description: "Search for medicine info",
    },
    {
        icon: <ArrowLeftRight size={16} />,
        label: "Give me substitutes for Combiflam",
        description: "Find alternatives by composition",
    },
    {
        icon: <MessageCircleQuestion size={16} />,
        label: "Which one is the cheapest among them?",
        description: "Ask follow-up questions",
    },
];

interface Props {
    onSuggestion: (text: string) => void;
}

export default function EmptyState({ onSuggestion }: Props) {
    return (
        <div className="flex-1 flex flex-col items-center justify-center px-4 pb-8">
            <motion.div
                className="text-center max-w-md"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                {/* Emblem */}
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-teal-500 to-cyan-600 flex items-center justify-center shadow-xl mx-auto mb-5">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="white"
                        className="w-8 h-8"
                    >
                        <path d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
                    </svg>
                </div>

                <h2 className="text-2xl font-bold text-slate-800 mb-2">
                    AI Pharma Assistant
                </h2>
                <p className="text-sm text-slate-500 mb-8 leading-relaxed">
                    Search for medicines, find substitutes, compare prices, and get
                    intelligent drug information — all in one place.
                </p>

                {/* Suggestion chips */}
                <div className="flex flex-col gap-2 text-left">
                    {suggestions.map((s, i) => (
                        <motion.button
                            key={i}
                            onClick={() => onSuggestion(s.label)}
                            className="flex items-center gap-3 bg-white hover:bg-teal-50 border border-slate-200 hover:border-teal-300 rounded-xl px-4 py-3 transition-all duration-200 text-left group"
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.1 * i + 0.3, duration: 0.3 }}
                        >
                            <span className="text-teal-500 group-hover:text-teal-600 flex-shrink-0">
                                {s.icon}
                            </span>
                            <div className="min-w-0">
                                <p className="text-sm font-medium text-slate-700 truncate">
                                    {s.label}
                                </p>
                                <p className="text-xs text-slate-400">{s.description}</p>
                            </div>
                        </motion.button>
                    ))}
                </div>
            </motion.div>
        </div>
    );
}
