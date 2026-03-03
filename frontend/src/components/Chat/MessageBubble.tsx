"use client";

import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Message } from "@/types/chat";

interface Props {
    message: Message;
}

export default function MessageBubble({ message }: Props) {
    const isUser = message.role === "user";

    return (
        <motion.div
            className={`flex items-end gap-3 mb-4 ${isUser ? "flex-row-reverse" : "flex-row"}`}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
        >
            {/* Avatar */}
            {!isUser && (
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-teal-500 to-cyan-600 flex items-center justify-center shadow-md">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="white"
                        className="w-4 h-4"
                    >
                        <path d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
                    </svg>
                </div>
            )}

            {/* Bubble */}
            <div
                className={`max-w-[75%] rounded-2xl px-4 py-3 shadow-sm text-sm leading-relaxed ${isUser
                        ? "bg-gradient-to-br from-teal-500 to-cyan-600 text-white rounded-br-sm"
                        : "bg-white border border-slate-100 text-slate-800 rounded-bl-sm"
                    }`}
            >
                {isUser ? (
                    <p className="whitespace-pre-wrap">{message.content}</p>
                ) : (
                    <div className="prose prose-sm max-w-none prose-headings:text-slate-800 prose-p:text-slate-700 prose-strong:text-slate-900 prose-li:text-slate-700">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                            {message.content}
                        </ReactMarkdown>
                    </div>
                )}
            </div>

            {/* User avatar placeholder for alignment */}
            {isUser && (
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-slate-400 to-slate-500 flex items-center justify-center shadow-md">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="white"
                        className="w-4 h-4"
                    >
                        <path
                            fillRule="evenodd"
                            d="M7.5 6a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM3.751 20.105a8.25 8.25 0 0116.498 0 .75.75 0 01-.437.695A18.683 18.683 0 0112 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 01-.437-.695z"
                            clipRule="evenodd"
                        />
                    </svg>
                </div>
            )}
        </motion.div>
    );
}
