/**
 * Currency symbol utility — infers currency from ticker suffix.
 * Used by TechnicalAnalysisCard, OracleForecastCard, and PriceTimeseriesCard.
 * Completely isolated — no agent, no state, no LLM.
 */

const SYMBOL_MAP: Record<string, string> = {
    USD: "$", INR: "₹", GBP: "£", EUR: "€", JPY: "¥", CNY: "¥",
    KRW: "₩", HKD: "HK$", SGD: "S$", AUD: "A$", CAD: "C$",
};

/** Resolve currency symbol from a currency code (e.g. "INR" → "₹") */
export function getCurrencySymbol(code: string): string {
    return SYMBOL_MAP[code] || `${code} `;
}

/** Infer currency code from a ticker string (e.g. "MISHT.NS" → "INR", "AAPL" → "USD") */
export function inferCurrencyFromTicker(ticker?: string): string {
    if (!ticker) return "USD";
    const t = ticker.toUpperCase();
    if (t.endsWith(".NS") || t.endsWith(".BO")) return "INR";
    if (t.endsWith(".L")) return "GBP";
    if (t.endsWith(".PA") || t.endsWith(".DE")) return "EUR";
    if (t.endsWith(".T")) return "JPY";
    if (t.endsWith(".HK")) return "HKD";
    if (t.endsWith(".SI")) return "SGD";
    if (t.endsWith(".AX")) return "AUD";
    if (t.endsWith(".TO")) return "CAD";
    return "USD";
}

/** Convenience: ticker → symbol (e.g. "RPOWER.NS" → "₹") */
export function currencySymbolForTicker(ticker?: string): string {
    return getCurrencySymbol(inferCurrencyFromTicker(ticker));
}

/** Format a number with the right currency symbol */
export function formatPrice(value: number | undefined | null, ticker?: string): string {
    if (value == null) return "---";
    const sym = currencySymbolForTicker(ticker);
    return `${sym}${value.toLocaleString()}`;
}
