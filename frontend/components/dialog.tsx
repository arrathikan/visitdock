"use client";
import { useEffect, useRef } from "react";
export default function Modal({ title, children, close, busy = false, drawer = false }: { title: string; children: React.ReactNode; close: () => void; busy?: boolean; drawer?: boolean }) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    const element = ref.current;
    const previous = document.activeElement as HTMLElement | null;
    element?.showModal();
    return () => { element?.close(); previous?.focus(); };
  }, []);
  return <dialog ref={ref} className={drawer ? "drawer" : "confirm"} aria-labelledby="dialog-title" onCancel={event => { event.preventDefault(); if (!busy) close(); }}>
    <div className="dialoghead"><h2 id="dialog-title">{title}</h2><button type="button" aria-label="Close dialog" disabled={busy} onClick={close}>×</button></div>{children}
  </dialog>;
}
