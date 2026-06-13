// reusable button component
// poore project me same luxury button style use hoga

function Button({
  text,
  type = "button",
  onClick,
  variant = "primary",
  fullWidth = false,
  disabled = false,
  className = "",
}) {
  const baseStyle =
    "inline-flex items-center justify-center rounded-full px-7 py-3 text-[11px] font-bold uppercase tracking-widest transition-all duration-300 disabled:opacity-60 disabled:cursor-not-allowed";

  const variants = {
    primary:
      "bg-[#0A1A2F] text-white hover:bg-[#C9A03D] hover:text-[#0A1A2F]",
    gold:
      "bg-[#C9A03D] text-[#0A1A2F] hover:bg-[#0A1A2F] hover:text-white",
    outline:
      "border border-[#0A1A2F] text-[#0A1A2F] hover:bg-[#0A1A2F] hover:text-white",
    light:
      "border border-white text-white hover:bg-white hover:text-[#0A1A2F]",
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyle} ${variants[variant]} ${
        fullWidth ? "w-full" : ""
      } ${className}`}
    >
      {text}
    </button>
  );
}

export default Button;