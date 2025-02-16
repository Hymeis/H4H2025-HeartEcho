'use client';
import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

function getRandomChar() {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+{}|:<>?";
    const randomIndex = Math.floor(Math.random() * chars.length);
    return chars[randomIndex];
}

export default function LoadingScreen() {
    const phrases = [
        "Loading...",
    ];

    const [displayedText, setDisplayedText] = useState("");
    
    useEffect(() => {
        let isCancelled = false; // so we can cancel animation on unmount
    
        async function cyclePhrases() {
        while (!isCancelled) {
            for (const phrase of phrases) {
                if (isCancelled) break;
                await animatePhrase(phrase);
            }
        }
        }
    
        cyclePhrases();
    
        // Avoid memory leak
        return () => {
            isCancelled = true;
        };
    }, []);

    const animatePhrase = async (phrase: string) => {
        const length = phrase.length;
        const encodedArray = Array(length).fill(""); // holds the random chars
        const currentArray = Array(length).fill(""); // what we'll display at each step
    
        // 1) ENCODE STAGE
        for (let i = 0; i < length; i++) {
            if (encodedArray[i] === "") {
                encodedArray[i] = getRandomChar();
            }
            currentArray[i] = encodedArray[i];
            setDisplayedText(currentArray.join(""));
            await waitMs(15);
        }
    
        // 2) DECODE STAGE
        for (let i = 0; i < length; i++) {
            currentArray[i] = phrase[i];
            setDisplayedText(currentArray.join(""));
            await waitMs(20);
        }
    
        await waitMs(1000);
    
        // 3) EXIT STAGE
        for (let i = length - 1; i >= 0; i--) {
            currentArray[i] = "";
            setDisplayedText(currentArray.join(""));
            await waitMs(10);
        }
    };
    
    const waitMs = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

    return (
        <motion.div
        className="fixed inset-0 flex items-center justify-center bg-black z-50"
        initial={{ opacity: 1 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        >
            <p className="text-3xl text-white max-w-2xl text-center min-h-[1em]">
                {displayedText}
            </p>
        </motion.div>
    );
}
