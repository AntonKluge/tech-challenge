namespace Typography {
  export function H1({ children }: { children: React.ReactNode }) {
    return <h1 className="text-3xl font-bold tracking-tight">{children}</h1>;
  }

  export function H2({ children }: { children: React.ReactNode }) {
    return (
      <h2 className="text-2xl font-semibold tracking-tight first:mt-0">
        {children}
      </h2>
    );
  }
}

export default Typography;
