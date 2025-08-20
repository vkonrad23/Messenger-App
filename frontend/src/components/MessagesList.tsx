import React from 'react';

type Message = {
  id: string;
  text: string;
  // Use whichever your API provides:
  isDeleted?: boolean;
  deletedAt?: string | null;
};

export function MessagesList({ messages }: { messages: Message[] }) {
  const visible = messages.filter((m) => !m.isDeleted && !m.deletedAt);
  return (
    <div className="flex flex-col gap-2">
      {visible.map((m) => (
        <div key={m.id} className="rounded bg-gray-100 p-2">
          {m.text}
        </div>
      ))}
    </div>
  );
}
