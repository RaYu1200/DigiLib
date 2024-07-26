import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './dashboard.component';
import { AddFileComponent } from './add-file/add-file.component';
import { SearchComponent } from './search/search.component';


const reportsdRoutes: Routes = [
    {
        path: '',
        component: DashboardComponent,
        children: [
            {
                path :'upload',
                title: 'DRM Upload',
                component : AddFileComponent
            },
            {
                path:'search',
                title: 'DRM Search',
                component: SearchComponent
            },
            {
                path : '',
                redirectTo : 'upload',
                pathMatch : 'full'
            }
        ]
            
    }
];

@NgModule({
    imports: [
        RouterModule.forChild(reportsdRoutes)
    ],
    exports: [
        RouterModule
    ]
})
export class DashboardRoutingModule { }
