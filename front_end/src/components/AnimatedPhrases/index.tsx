"use client";

import { useEffect, useState } from "react";

function getRandomChar() {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+{}|:<>?";
  const randomIndex = Math.floor(Math.random() * chars.length);
  return chars[randomIndex];
}

export default function AnimatedPhrases() {
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

    // Cleanup to avoid memory leaks if component unmounts
    return () => {
      isCancelled = true;
    };
  }, []);

  /**
   * Animate one phrase:
   * 1) Encode: type random characters (one by one) until the phrase length is reached.
   * 2) Decode: swap each random char with the actual phrase char.
   * 3) Exit: remove each character from right to left.
   */
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
      await waitMs(10);
    }

    // 2) DECODE STAGE
    for (let i = 0; i < length; i++) {
      currentArray[i] = phrase[i];
      setDisplayedText(currentArray.join(""));
      await waitMs(10);
    }

    await waitMs(2000);

    // 3) EXIT STAGE
    for (let i = length - 1; i >= 0; i--) {
      currentArray[i] = "";
      setDisplayedText(currentArray.join(""));
      await waitMs(10);
    }

  };

  const waitMs = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

  return (
    <p className="text-lg text-white max-w-2xl text-center min-h-[1em]">
      {displayedText}
    </p>
  );
}
