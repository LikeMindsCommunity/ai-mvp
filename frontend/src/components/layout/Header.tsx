import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store';
import { logout } from '../../store/slices/userSlice';
import { Button } from '../ui/button';
import {
    Avatar,
    AvatarImage,
    AvatarFallback,
} from '../ui/avatar';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '../ui/dropdown-menu';

const Header: React.FC = () => {
    const dispatch = useDispatch();
    const { user, isAuthenticated } = useSelector((state: RootState) => state.user);
    const { currentMode } = useSelector((state: RootState) => state.mode);

    const handleLogout = () => {
        dispatch(logout());
    };

    return (
        <header className="sticky top-0 z-40 w-full border-b bg-white dark:bg-slate-900 shadow-sm">
            <div className="container flex h-16 items-center px-4 sm:px-6 lg:px-8">
                <div className="mr-4 flex">
                    <a href="/" className="flex items-center space-x-2">
                        <span className="font-bold text-xl text-slate-900 dark:text-white">
                            LikeMinds Assistant
                        </span>
                    </a>
                </div>

                <div className="flex flex-1 items-center justify-between space-x-4">
                    <nav className="flex items-center space-x-4">
                        <span className="text-sm font-medium text-slate-600 dark:text-slate-300">
                            {currentMode === 'documentation' ? 'Documentation Mode' : 'Coding Mode'}
                        </span>
                    </nav>

                    <div className="flex items-center space-x-4">
                        {isAuthenticated ? (
                            <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                    <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                                        <Avatar className="h-8 w-8">
                                            <AvatarImage src={user?.picture} alt={user?.name || 'User avatar'} />
                                            <AvatarFallback>{user?.name?.[0] || 'U'}</AvatarFallback>
                                        </Avatar>
                                    </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent align="end">
                                    <DropdownMenuLabel>My Account</DropdownMenuLabel>
                                    <DropdownMenuSeparator />
                                    <DropdownMenuItem>Profile</DropdownMenuItem>
                                    <DropdownMenuItem>Settings</DropdownMenuItem>
                                    <DropdownMenuSeparator />
                                    <DropdownMenuItem onClick={handleLogout}>
                                        Log out
                                    </DropdownMenuItem>
                                </DropdownMenuContent>
                            </DropdownMenu>
                        ) : (
                            <Button variant="default">Sign In</Button>
                        )}
                    </div>
                </div>
            </div>
        </header>
    );
};

export default Header; 