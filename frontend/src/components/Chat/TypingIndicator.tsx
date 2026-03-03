"use client";

import { motion } from "framer-motion";

export default function TypingIndicator() {
    return (
        <div className="flex items-end gap-3 mb-4">
            {/* Bot avatar */}
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
            {/* Bubble */}
            <div className="bg-white border border-slate-100 rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm">
                <div className="flex items-center gap-1.5">
                    {[0, 1, 2].map((i) => (
                        <motion.span
                            key={i}
                            className="block w-2 h-2 rounded-full bg-teal-400"
                            animate={{ y: ["0%", "-50%", "0%"], opacity: [0.5, 1, 0.5] }}
                            transition={{
                                duration: 0.9,
                                repeat: Infinity,
                                ease: "easeInOut",
                                delay: i * 0.18,
                            }}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}
