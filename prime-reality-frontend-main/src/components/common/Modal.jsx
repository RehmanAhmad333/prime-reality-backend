// reusable modal component
// forms, confirmation aur popup ke liye use hoga

function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] bg-black/70 backdrop-blur-sm flex items-center justify-center px-4">
      <div className="relative w-full max-w-lg bg-white rounded-[28px] p-6 shadow-2xl">
        <button
          type="button"
          onClick={onClose}
          className="absolute right-5 top-4 text-2xl font-bold text-[#333333] hover:text-[#EF4444]"
        >
          ×
        </button>

        <h2 className="font-heading text-2xl font-bold text-[#0A1A2F] mb-5">
          {title}
        </h2>

        {children}
      </div>
    </div>
  );
}

export default Modal;