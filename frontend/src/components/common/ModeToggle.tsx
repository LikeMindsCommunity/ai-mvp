import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '@/store';
import { setMode } from '@/store/slices/modeSlice';
import { Button } from '@/components/ui/button';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';

const ModeToggle: React.FC = () => {
    const dispatch = useDispatch();
    const { currentMode } = useSelector((state: RootState) => state.mode);

    const handleModeChange = (mode: 'documentation' | 'coding') => {
        dispatch(setMode(mode));
    };

    return (
        <div className="flex items-center justify-between">
            <Tabs
                value={currentMode}
                onValueChange={(value) => handleModeChange(value as 'documentation' | 'coding')}
                className="w-full max-w-[400px]"
            >
                <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="documentation" className="data-[state=active]:bg-violet-500 data-[state=active]:text-white">
                        Documentation
                    </TabsTrigger>
                    <TabsTrigger value="coding" className="data-[state=active]:bg-emerald-500 data-[state=active]:text-white">
                        Coding
                    </TabsTrigger>
                </TabsList>
            </Tabs>
        </div>
    );
};

export default ModeToggle; 