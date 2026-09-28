import { forwardRef, type ButtonHTMLAttributes, type HTMLAttributes } from 'react'; import { cn } from '../lib/utils';
export const Button = forwardRef<HTMLButtonElement, ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary'|'ghost' }>(({ className, variant='primary', ...props },ref) => <button ref={ref} className={cn(variant==='primary'?'btn-primary':'btn-ghost',className)} {...props}/>);
export const Card = ({className,...props}:HTMLAttributes<HTMLDivElement>) => <div className={cn('card',className)} {...props}/>;
export const Skeleton = ({className}: {className?:string}) => <div className={cn('animate-pulse rounded-xl bg-black/10 dark:bg-white/10',className)}/>;
