import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Combines Tailwind CSS class names cleanly using clsx and tailwind-merge.
 * Follows the Baseline UI skill standard.
 */
export function cn(...inputs) {
  return twMerge(clsx(inputs));
}
