import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../../store';
import Header from './Header';
import Sidebar from './Sidebar';
import ModeToggle from '../common/ModeToggle';

interface MainLayoutProps {
    children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
    const { isAuthenticated } = useSelector((state: RootState) => state.user);
    const { currentMode } = useSelector((state: RootState) => state.mode);

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
            <Header />

            <div className="flex">
                {isAuthenticated && (
                    <Sidebar />
                )}

                <main className="flex-1 p-6">
                    <div className="mb-6">
                        <ModeToggle />
                    </div>

                    <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg">
                        {children}
                    </div>
                </main>
            </div>

            <footer className="py-4 px-6 text-center text-sm text-slate-600 dark:text-slate-400">
                © {new Date().getFullYear()} LikeMinds. All rights reserved.
            </footer>
        </div>
    );
};

export default MainLayout; 